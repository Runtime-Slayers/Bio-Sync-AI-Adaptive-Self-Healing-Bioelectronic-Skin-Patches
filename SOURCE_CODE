/*
  BioSync-AI: Bar Graph Dosing Version
  - Replaced Servo with LED Bar Graph
  - Relay acts as "Safety Interlock" cutting Ground to the LEDs
  
  WIRING:
  - Bar Graph Anodes 1-5 -> GPIO 14, 15, 16, 17, 18
  - Bar Graph Cathodes   -> Connected together -> Relay NO
  - Relay COM            -> GND
  - Relay IN             -> GPIO 13
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

// =======================
// PIN MAPPING
// =======================
#define SDA_PIN    8
#define SCL_PIN    9
#define POT_PIN    4    // Infection Sensor
#define RELAY_PIN  13   // Safety Switch
#define PIXEL_PIN  5    // LED Ring
#define BREACH_PIN 7    // Slide Switch
#define BUZZ_PIN   10   // Buzzer

// Bar Graph Pins (5 Segments)
const int barGraphPins[] = {14, 15, 16, 17, 18}; 

// =======================
// CONFIGURATION
// =======================
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define NUMPIXELS 16

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Adafruit_NeoPixel pixels(NUMPIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

// =======================
// VARIABLES
// =======================
unsigned long lastPageChange = 0;
int currentPage = 0;
int graphBuffer[128];
int bufferIdx = 0;
String patientCondition = "ANALYZING...";

// ECG Animation Vars
unsigned long lastBeatTime = 0;
int beatPhase = 0;
int baseLine = 40;

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);

  // 1. Init OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { for(;;); }
  display.clearDisplay();

  // 2. Init Bar Graph Pins
  for(int i=0; i<5; i++) {
    pinMode(barGraphPins[i], OUTPUT);
    digitalWrite(barGraphPins[i], LOW);
  }

  // 3. Init Relay (Safety)
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Start Disconnected (Safe)

  // 4. Init Other Hardware
  pixels.begin(); pixels.show();
  pinMode(BREACH_PIN, INPUT_PULLUP);
  pinMode(BUZZ_PIN, OUTPUT);

  // 5. Intro Screen
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(30, 20);
  display.println(F("BIOSYNC-AI"));
  display.setCursor(20, 30);
  display.println(F("DOSING GAUGE"));
  display.display();
  
  // ==========================================
  // BOOT SELF-TEST (Bar Graph Animation)
  // ==========================================
  tone(BUZZ_PIN, 1000, 100);
  digitalWrite(RELAY_PIN, HIGH); // Enable Ground Path
  
  // Fill up the gauge
  for(int i=0; i<5; i++) {
    digitalWrite(barGraphPins[i], HIGH);
    delay(150);
  }
  delay(500);
  // Empty the gauge
  for(int i=4; i>=0; i--) {
    digitalWrite(barGraphPins[i], LOW);
    delay(100);
  }
  
  digitalWrite(RELAY_PIN, LOW); // Disable Ground Path
  
  // Init graph buffer
  for (int i = 0; i < 128; i++) graphBuffer[i] = baseLine;
}

void loop() {
  // --- SENSING ---
  int rawBio = analogRead(POT_PIN);         
  bool isBreach = !digitalRead(BREACH_PIN); 

  // --- ECG ANIMATION ---
  int beatInterval = map(rawBio, 0, 4095, 1200, 300);
  if (millis() - lastBeatTime > beatInterval) { lastBeatTime = millis(); beatPhase = 1; }
  
  int currentSignal = baseLine;
  if (beatPhase > 0) {
    if(beatPhase==2) currentSignal -= 25; // Spike
    else if(beatPhase==3) currentSignal += 15;
    else currentSignal = baseLine;
    beatPhase = (beatPhase > 5) ? 0 : beatPhase + 1;
  }
  if(rawBio > 2000) currentSignal += random(-2, 3);
  graphBuffer[bufferIdx] = currentSignal;
  bufferIdx = (bufferIdx + 1) % 128;

  // --- DIAGNOSIS ---
  if (isBreach) patientCondition = "CRITICAL FAILURE";
  else if (rawBio < 1500) patientCondition = "STABLE / SAFE";
  else if (rawBio < 3000) patientCondition = "INFECTION DETECTED";
  else patientCondition = "HIGH VIRAL LOAD";

  // --- SAFETY & BAR GRAPH LOGIC ---
  
  // CASE 1: BREACH (Hardware Cutoff)
  if (isBreach) {
    digitalWrite(RELAY_PIN, LOW); // CUT GROUND -> Gauge goes DEAD physically
    setRingColor(255, 0, 0);      // Red Ring
    tone(BUZZ_PIN, 2000);
    updateBarGraph(0);            // Software also sets 0
  }
  
  // CASE 2: HIGH INFECTION (Max Dose)
  else if (rawBio >= 3000) {
    digitalWrite(RELAY_PIN, HIGH); // Enable Gauge
    setRingColor(255, 140, 0);     // Orange Ring
    if (millis() % 500 < 250) tone(BUZZ_PIN, 1000); else noTone(BUZZ_PIN);
    updateBarGraph(5);             // 5 Bars (FULL)
  }
  
  // CASE 3: MILD INFECTION (Variable Dose)
  else if (rawBio >= 1500) {
    digitalWrite(RELAY_PIN, HIGH); // Enable Gauge
    setRingColor(0, 0, 255);       // Blue Ring
    noTone(BUZZ_PIN);
    
    // Map infection 1500-3000 to 1-4 Bars
    int bars = map(rawBio, 1500, 3000, 1, 4);
    updateBarGraph(bars);
  }
  
  // CASE 4: HEALTHY (Standby)
  else {
    digitalWrite(RELAY_PIN, LOW);  // Power Save
    updateBarGraph(0);
    
    // Breathing Green
    int b = (millis() / 20) % 255; 
    if(b > 127) b = 255 - b;
    setRingColor(0, map(b,0,127,0,100), 0);
    noTone(BUZZ_PIN);
  }

  // --- DISPLAY ---
  bool lock = isBreach;
  if (!lock && millis() - lastPageChange > 3000) {
    currentPage = (currentPage + 1) % 3;
    lastPageChange = millis();
  }

  display.clearDisplay();
  if (isBreach) drawAlert("DEVICE FAILURE");
  else {
    if (currentPage == 0) drawPatient(rawBio);
    else if (currentPage == 1) drawAgent(rawBio);
    else drawGraph();
  }
  display.display();
  delay(30); 
}

// --- HELPER: Control Bar Graph Segments ---
void updateBarGraph(int level) {
  for(int i=0; i<5; i++) {
    if(i < level) digitalWrite(barGraphPins[i], HIGH);
    else digitalWrite(barGraphPins[i], LOW);
  }
}

// --- DRAWING HELPERS ---
void drawPatient(int val) {
  display.setCursor(0,0); display.print(F("PT ID: #8492-X"));
  display.drawLine(0,8,128,8,WHITE);
  display.setCursor(0,20); display.print(F("STATUS:"));
  display.setCursor(0,30); display.print(patientCondition);
  display.setCursor(0,50); display.print(F("Dose: "));
  
  // Show graphical bar on OLED too
  int bars = 0;
  if(digitalRead(RELAY_PIN) == HIGH) {
     if(val >= 3000) bars = 5;
     else if(val >= 1500) bars = map(val, 1500, 3000, 1, 4);
  }
  for(int i=0; i<5; i++) {
    if(i<bars) display.fillRect(40 + (i*10), 50, 8, 8, WHITE);
    else display.drawRect(40 + (i*10), 50, 8, 8, WHITE);
  }
}

void drawAgent(int val) {
  display.setCursor(0,0); display.print(F("AGENT CORE"));
  display.drawLine(0,8,128,8,WHITE);
  display.setCursor(0,20); display.print(F("AI Model: Active"));
  display.setCursor(0,30); display.print(F("Latency: 12ms"));
  display.setCursor(0,50); display.print(F("Confidence: 99%"));
}

void drawGraph() {
  display.setCursor(0,0); display.print(F("LIVE BIOSIGNAL"));
  for (int i=0; i<127; i++) {
    int idx = (bufferIdx + i) % 128;
    int next = (idx + 1) % 128;
    display.drawLine(i, graphBuffer[idx], i+1, graphBuffer[next], WHITE);
  }
}

void drawAlert(String msg) {
  display.fillScreen(BLACK);
  display.drawRect(0,0,128,64,WHITE);
  display.setCursor(10,20); display.setTextSize(2); display.print(F("!ALERT!"));
  display.setTextSize(1); display.setCursor(10,45); display.print(msg);
}

void setRingColor(int r, int g, int b) {
  for(int i=0; i<NUMPIXELS; i++) pixels.setPixelColor(i, pixels.Color(r,g,b));
  pixels.show();
}
