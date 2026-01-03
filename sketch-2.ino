/*
  BioSync-AI: ADVANCED MEDICAL DASHBOARD (10s Recovery Edition)
  - Sensor: Potentiometer on Pin 4 (0-4095 mapped to 70-400 mg/dL)
  - OLED: Quad-Panel Telemetry (Graph, BPM, Doses, Status)
  - Logic: 10-Second Delay after 50ml cycle completion.
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>
#include <LiquidCrystal_I2C.h>

// =======================
// 1. PIN CONFIGURATION
// =======================
#define POT_PIN      4     
#define BREACH_PIN   7     
#define RELAY_PIN    13    
#define BUZZ_PIN     10    
#define PIXEL_PIN    5     
const int barGraphPins[] = {35, 36, 37, 38, 39}; 

// =======================
// 2. SYSTEM CONSTANTS
// =======================
#define OLED_ADDR    0x3C
#define LCD_ADDR     0x27  
#define NUMPIXELS    16
#define SAMPLE_RATE  100

// =======================
// 3. GLOBAL VARIABLES
// =======================
float simulatedGlucose = 100.0;
unsigned long lastSampleTime = 0;
int medicineTank = 200; 
int patientIntake = 0;  
int completedDoses = 0; 
int graphBuffer[128]; 
int bufferIdx = 0;

// State Logic
const long DOSE_DURATION = 3000;    
const long RECOVERY_TIME = 10000;   // <--- UPDATED: 10 Second Safety Delay
unsigned long doseStartTime = 0;
bool isDosing = false;
bool isRecovering = false;
int activeBars = 0;                 
int snapshotBars = 0;

Adafruit_SSD1306 oled(128, 64, &Wire, -1);
LiquidCrystal_I2C lcd(LCD_ADDR, 16, 2); 
Adafruit_NeoPixel pixels(NUMPIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Wire.begin(8, 9); 
  oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  oled.clearDisplay();
  
  lcd.init(); 
  lcd.backlight();
  
  for(int i=0; i<5; i++) pinMode(barGraphPins[i], OUTPUT);
  pinMode(RELAY_PIN, OUTPUT); 
  pinMode(BREACH_PIN, INPUT_PULLUP);
  pinMode(BUZZ_PIN, OUTPUT);

  pixels.begin();
  pixels.show();

  for(int i=0; i<128; i++) graphBuffer[i] = 45; 
  updateLCD(); 
}

void loop() {
  unsigned long currentMillis = millis();

  // 1. DATA ACQUISITION
  if (currentMillis - lastSampleTime >= SAMPLE_RATE) {
    lastSampleTime = currentMillis;
    
    int rawPot = analogRead(POT_PIN);
    simulatedGlucose = map(rawPot, 0, 4095, 70, 400);

    // Dose Gauge Threshold Logic
    if (simulatedGlucose < 120) activeBars = 0;
    else if (simulatedGlucose < 140) activeBars = 1;
    else if (simulatedGlucose < 160) activeBars = 2;
    else if (simulatedGlucose < 190) activeBars = 3;
    else if (simulatedGlucose < 230) activeBars = 4;
    else activeBars = 5;

    // Update Waveform Buffer (Does not disturb display)
    graphBuffer[bufferIdx] = map((int)simulatedGlucose, 70, 400, 60, 20);
    bufferIdx = (bufferIdx + 1) % 128;
  }

  // 2. DOSING ENGINE & RECOVERY
  checkDosingLogic();

  // 3. UI UPDATES
  updateHardwareVisuals();
  renderOLED();
}

void checkDosingLogic() {
  bool isBreach = !digitalRead(BREACH_PIN);

  // TRIGGER: System starts dose if not in Recovery/Breach
  if (!isBreach && !isDosing && !isRecovering && activeBars > 0) {
    isDosing = true;
    doseStartTime = millis();
    snapshotBars = activeBars; 
    digitalWrite(RELAY_PIN, HIGH); 
    
    int doseAmount = snapshotBars * 10;
    
    // Check for 50ml cycle completion
    if (patientIntake + doseAmount >= 50) {
        int needed = 50 - patientIntake;
        medicineTank -= needed;
        patientIntake = 0; 
        completedDoses++; 
        tone(BUZZ_PIN, 2000, 500); // Success tone
    } else {
        patientIntake += doseAmount;
        medicineTank -= doseAmount;
        tone(BUZZ_PIN, 1200, 100); // Standard infusion tone
    }

    if (medicineTank <= 0) medicineTank = 200; 
    updateLCD(); 
  }

  // DOSE COMPLETION -> Start 10s Recovery
  if (isDosing && (millis() - doseStartTime > DOSE_DURATION)) {
    isDosing = false;
    isRecovering = true;
    digitalWrite(RELAY_PIN, LOW); 
  }

  // END OF 10s RECOVERY
  if (isRecovering && (millis() - doseStartTime > (DOSE_DURATION + RECOVERY_TIME))) {
    isRecovering = false;
  }
}

void renderOLED() {
  oled.clearDisplay();
  oled.setTextColor(WHITE);
  
  if (!digitalRead(BREACH_PIN)) {
    oled.drawRect(0,0,128,64,WHITE);
    oled.setCursor(35, 25); oled.print("BREACH!");
  } else {
    // 1. LIVE WAVEFORM (Top Half)
    for (int i = 0; i < 127; i++) {
      oled.drawLine(i, graphBuffer[(bufferIdx+i)%128], i+1, graphBuffer[(bufferIdx+i+1)%128], WHITE);
    }
    
    // 2. DATA PANEL (Bottom Half)
    oled.drawFastHLine(0, 48, 128, WHITE);
    oled.setCursor(0, 52); oled.print((int)simulatedGlucose); oled.print(" mg/dL");
    oled.setCursor(70, 52); oled.print("D-COMP:"); oled.print(completedDoses);
    
    // 3. VITALS & MODE (Header)
    oled.setCursor(0, 0); oled.print("BPM: "); 
    oled.print(map((int)simulatedGlucose, 70, 400, 72, 115)); 
    
    oled.setCursor(75, 0);
    if(isDosing) oled.print("INFUSING");
    else if(isRecovering) oled.print("10s DELAY");
    else oled.print("MONITOR");
  }
  oled.display();
}

void updateLCD() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Tank: "); lcd.print(medicineTank); lcd.print("ml");
  lcd.setCursor(0,1);
  lcd.print("Dose: "); lcd.print(patientIntake); lcd.print("/50ml");
}

void updateHardwareVisuals() {
  bool isBreach = !digitalRead(BREACH_PIN);
  uint32_t ringColor;
  
  if (isBreach) ringColor = pixels.Color(255, 0, 0);
  else if (isDosing) {
    // 1-3 bars = Blue, 4-5 bars = Orange
    ringColor = (snapshotBars <= 3) ? pixels.Color(0, 150, 255) : pixels.Color(255, 100, 0);
  } else if (isRecovering) {
    // Pulsing Cyan for 10s Recovery
    int b = (millis()/50)%255; if(b>127) b=255-b;
    ringColor = pixels.Color(0, map(b,0,127,0,150), 200);
  } else {
    ringColor = pixels.Color(0, 100, 0); // Steady Green
  }

  for(int i=0; i<NUMPIXELS; i++) pixels.setPixelColor(i, ringColor);
  pixels.show();

  int displayBars = isDosing ? snapshotBars : activeBars;
  for(int i=0; i<5; i++) {
    digitalWrite(barGraphPins[i], (isDosing && i < displayBars) ? HIGH : LOW);
  }
}