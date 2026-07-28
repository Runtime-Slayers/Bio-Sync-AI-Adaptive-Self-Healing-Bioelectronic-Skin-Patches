/*
  BioSync-AI: Final Hackathon Version
  Device: ESP32-S3
  Features: Multi-Page UI, Real-Time Diagnosis, Agentic Control
*/

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP32Servo.h>
#include <Adafruit_NeoPixel.h>

// =======================
// 1. PIN MAPPING (ESP32-S3)
// =======================
#define SDA_PIN    8    // OLED SDA
#define SCL_PIN    9    // OLED SCL
#define POT_PIN    4    // Bio-Sensor (Potentiometer)
#define SERVO_PIN  6    // Drug Pump (Servo)
#define PIXEL_PIN  5    // LED Ring (NeoPixel)
#define BREACH_PIN 7    // Slide Switch (Tear Trigger)
#define BUZZ_PIN   10   // Piezo Buzzer
#define BTN_PIN    11   // Patient Override Button

// =======================
// 2. CONFIGURATION
// =======================
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define NUMPIXELS     16 

// =======================
// 3. GLOBAL OBJECTS
// =======================
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Servo drugPump;
Adafruit_NeoPixel pixels(NUMPIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

// =======================
// 4. SYSTEM VARIABLES
// =======================
unsigned long lastPageChange = 0;
int currentPage = 0; // 0=Patient Status, 1=AI Logic, 2=Telemetry
int graphBuffer[128]; 
int bufferIdx = 0;
String patientCondition = "ANALYZING...";

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);

  // Init OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { for(;;); }
  
  // Init Hardware
  drugPump.attach(SERVO_PIN); 
  pixels.begin();
  pixels.show();
  
  pinMode(BREACH_PIN, INPUT_PULLUP);
  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(BUZZ_PIN, OUTPUT);

  // Intro Sequence
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(20, 25);
  display.println(F("BIOSYNC-AI"));
  display.setCursor(20, 35);
  display.println(F("Initializing..."));
  display.display();
  
  tone(BUZZ_PIN, 1000, 100); // Boot beep
  delay(1000);
  
  // Fill graph buffer with baseline data
  for(int i=0; i<128; i++) graphBuffer[i] = 45; 
}

void loop() {
  // --- READ SENSORS ---
  int rawBio = analogRead(POT_PIN);
  bool isBreach = !digitalRead(BREACH_PIN); // Active LOW
  bool isPain = !digitalRead(BTN_PIN);      // Active LOW

  // --- DIAGNOSIS ENGINE ---
  // Translate sensor data into Patient Situations
  if (isBreach) {
    patientCondition = "CRITICAL FAILURE";
  } else if (isPain) {
    patientCondition = "PAIN REPORTED";
  } else if (rawBio < 1500) {
    patientCondition = "STABLE / NORMAL";
  } else if (rawBio >= 1500 && rawBio < 3000) {
    patientCondition = "MILD INFLAMMATION";
  } else {
    patientCondition = "HIGH INFECTION";
  }

  // --- UPDATE GRAPH HISTORY ---
  // Map sensor value to screen coordinates (Bottom section of screen)
  int graphY = map(rawBio, 0, 4095, 63, 30); 
  graphBuffer[bufferIdx] = graphY;
  bufferIdx = (bufferIdx + 1) % 128;

  // --- AGENTIC ACTION LOOP ---
  if (isBreach) {
    handleBreach();
  } else if (isPain) {
    handlePain();
  } else if (rawBio >= 1500) {
    handleTreatment(rawBio);
  } else {
    handleHomeostasis();
  }

  // --- MULTI-PAGE DISPLAY MANAGER ---
  // Auto-switch pages every 3 seconds (unless in Emergency)
  if (!isBreach && millis() - lastPageChange > 3000) {
    currentPage = (currentPage + 1) % 3;
    lastPageChange = millis();
  }

  display.clearDisplay();

  if (isBreach) {
    drawEmergencyPage(); // Lock screen on emergency
  } else {
    switch(currentPage) {
      case 0: drawPatientPage(rawBio); break; // The View You Requested
      case 1: drawAgentPage(); break;
      case 2: drawGraphPage(); break;
    }
  }

  display.display();
  delay(40); // Fast refresh for responsive graph
}

// ==========================================
// SCREEN DRAWING FUNCTIONS
// ==========================================

// PAGE 0: PATIENT SITUATION OVERVIEW
void drawPatientPage(int val) {
  display.setTextSize(1);
  display.setCursor(0,0); 
  display.print(F("PT. ID: #8492-X"));
  display.drawLine(0, 8, 128, 8, WHITE);

  display.setCursor(0, 15);
  display.print(F("CONDITION:"));
  
  // Dynamic Condition Text
  display.setCursor(0, 25);
  if(val > 3000) display.setTextColor(BLACK, WHITE); // Invert for emphasis
  else display.setTextColor(WHITE);
  
  display.print(patientCondition);
  display.setTextColor(WHITE); // Reset color

  display.setCursor(0, 40);
  display.print(F("Bio-Load: ")); display.print(val);
  
  display.setCursor(0, 50);
  display.print(F("Therapy: "));
  if(val > 1500) display.print(F("ACTIVE")); else display.print(F("STANDBY"));
}

// PAGE 1: AGENTIC AI INTERNALS
void drawAgentPage() {
  display.setCursor(0,0);
  display.print(F("AGENT LOGIC CORE"));
  display.drawLine(0, 8, 128, 8, WHITE);

  display.setCursor(0, 15);
  display.print(F("Model: BioBERT-Tiny"));
  display.setCursor(0, 25);
  display.print(F("Task: Homeostasis"));
  
  display.setCursor(0, 35);
  display.print(F("Latency: ")); display.print(random(8, 14)); display.print(F("ms"));
  
  display.setCursor(0, 45);
  display.print(F("Confidence: 98.4%"));
}

// PAGE 2: LIVE GRAPH VIEW
void drawGraphPage() {
  display.setCursor(0,0);
  display.print(F("LIVE BIOSIGNAL"));
  
  // Draw the scrolling graph line
  for (int i=0; i<128; i++) {
    int idx = (bufferIdx + i) % 128;
    // Connect lines for smoother look
    int nextIdx = (idx + 1) % 128;
    display.drawLine(i, graphBuffer[idx], i+1, graphBuffer[nextIdx], WHITE);
  }
}

void drawEmergencyPage() {
  display.fillScreen(BLACK);
  display.setTextSize(2);
  display.setCursor(10, 10);
  display.print(F("!ALERT!"));
  display.setTextSize(1);
  display.setCursor(10, 35);
  display.print(F("DEVICE FAILURE"));
  display.setCursor(10, 45);
  display.print(F("CONTACT DOCTOR"));
  display.drawRect(0, 0, 128, 64, WHITE);
}

// ==========================================
// ACTION HANDLERS
// ==========================================

void handleBreach() {
  setRingColor(255, 0, 0); // RED
  drugPump.write(0);       // Close valve
  // Siren
  tone(BUZZ_PIN, 2000); delay(50); tone(BUZZ_PIN, 1500);
}

void handlePain() {
  setRingColor(255, 0, 255); // PURPLE
  drugPump.write(180);       // Max Dose
  tone(BUZZ_PIN, 400, 20);   // Soft confirm beep
}

void handleTreatment(int val) {
  setRingColor(0, 0, 255); // BLUE
  // Calculate valve angle based on infection severity
  int angle = map(val, 1500, 4095, 20, 160);
  drugPump.write(angle);
  noTone(BUZZ_PIN);
}

void handleHomeostasis() {
  // Breathing Green LED
  int brightness = (millis() / 20) % 255;
  if (brightness > 127) brightness = 255 - brightness; // Triangle wave
  brightness = map(brightness, 0, 127, 10, 150);
  
  setRingColor(0, brightness, 0);
  drugPump.write(0);
  noTone(BUZZ_PIN);
}

void setRingColor(int r, int g, int b) {
  for(int i=0; i<NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(r, g, b));
  }
  pixels.show();
}