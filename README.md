# BioSync-AI: Adaptive Self-Healing Bioelectronic Skin Patches

**Team:** RunTime Slayers  
**Project Status:** Wokwi Simulation

---

## About The Project

BioSync-AI is a revolutionary AIoT wearable interface designed to move healthcare from passive monitoring to autonomous preservation.

Unlike traditional wearables that only track vital signs, BioSync-AI utilizes a closed-loop "Sense-Synthesize-Act" architecture. It combines Edge-based Agentic AI to make real-time, autonomous decisions and Generative AI to synthesize personalized molecular healing protocols on the fly.

This repository contains the proof-of-concept simulation, demonstrating how an autonomous agent manages biological distress and material integrity failures in real-time using an ESP32-S3 architecture.

---

## Key Features

- Sense-Synthesize-Act Loop: A fully autonomous, closed-loop system that eliminates human latency in medical intervention.
- Agentic Edge AI: An autonomous agent running locally on the ESP32-S3 that prioritizes tasks between homeostasis, infection treatment, and self-repair based on immediate urgency.
- Generative Protocol Synthesis: Demonstrates how GenAI creates bespoke healing dosages based on real-time biomarker severity.
- Simulated Self-Healing Material: Detects physical breaches in the patch circuitry and instantly reroutes power while initiating a repair protocol.
- Multi-Modal Patient Interface: Provides real-time feedback via an OLED dashboard, haptic buzzer alerts, and an LED status ring.

---

## Technology Stack

Hardware: ESP32-S3 WROOM, SSD1306 OLED, NeoPixel Ring, Micro Servo, Analog/Digital Sensors

Edge AI Logic: C++ (Arduino framework), Finite State Machine (Agentic Behavior)

AI Concepts: Agentic AI (Autonomous Decision Making), Generative AI (Protocol Synthesis Proxy)

Simulation Tool: Wokwi Browser-Based Simulator

---

## System Architecture

The BioSync-AI architecture is built on tiered autonomy, ensuring life-critical decisions happen at the edge.

Physical Bio-Layer:
- Bio-Sensors (pH/Glucose) transmit raw signals to ESP32-S3 Edge Core
- Actuators (Drug/Stim) receive commands from the core
- Material Integrity Sensor detects breaches and sends signal to core

Edge Intelligence Layer:
- Perception Agent reads sensor inputs
- Generative Synthesis Engine creates healing protocols
- Decision engine executes appropriate actions
- Actuators carry out prescribed therapy

User Interface Layer:
- OLED Dashboard displays patient status, AI logic, and live biosignals
- Haptic/Audio Alerts provide real-time notifications
- LED Ring indicates system status with color coding

---

## Getting Started

Prerequisites

A modern web browser (Chrome/Firefox recommended).

No physical hardware required.

Quick Start

1. Go to Wokwi.com and start a new ESP32-S3 project.
2. Wire the circuit following the pin mapping below.
3. Add the required libraries from the Library Manager.
4. Copy the C++ code from src/main.cpp and paste it into the sketch.
5. Click "Start the simulation" button.

---

## Installation & Setup Steps

Step 1: Access Wokwi Simulator

Open your web browser and navigate to Wokwi.com. Sign up or log in with your GitHub/Google account. Click "Create New Project" and select "ESP32-S3".

Step 2: Set Up the Hardware (Circuit Wiring)

In the Wokwi diagram editor, create connections following the pin mapping below.

Component Connections:

SSD1306 OLED SDA/SCL -> GPIO 8/GPIO 9
Potentiometer (Sensor) Signal Pin -> GPIO 4
Micro Servo (Pump) PWM Pin -> GPIO 6
NeoPixel Ring (Stim) DIN Pin -> GPIO 5
Slide Switch (Breach) Common Pin -> GPIO 7 (connect other side to GND)
Buzzer Positive (+) -> GPIO 10
Push Button Pin 1 -> GPIO 11

Step 3: Install Libraries

In Wokwi's Library Manager, add the following:
- Adafruit GFX Library
- Adafruit SSD1306
- ESP32Servo
- Adafruit NeoPixel

Step 4: Upload Code

Navigate to the BioSync-AI GitHub repository. Open the file src/main.cpp. Copy the complete C++ code and paste it into the Wokwi sketch.ino file.

Step 5: Run Simulation

Click the green "Start the simulation" button. Wait for the OLED to complete the boot sequence. The system is now ready for testing.

---

## Pin Mapping & Wiring Guide

ESP32-S3 Pin Configuration:

GPIO 4: POT_PIN (Potentiometer - Bio-Sensor)
GPIO 5: PIXEL_PIN (NeoPixel Ring - LED Status)
GPIO 6: SERVO_PIN (Servo Motor - Drug Pump)
GPIO 7: BREACH_PIN (Slide Switch - Breach Detector)
GPIO 8: SDA_PIN (OLED Display)
GPIO 9: SCL_PIN (OLED Display)
GPIO 10: BUZZ_PIN (Piezo Buzzer)
GPIO 11: BTN_PIN (Push Button - Pain Override)

I2C Address: 0x3C (OLED SSD1306)

Component Specifications:

SSD1306 OLED: 128x64 pixels, I2C (0x3C) - Real-time patient dashboard
Potentiometer: 10kohm linear - Bio-marker simulation (0-4095 ADC)
Micro Servo: 5V, 180-degree rotation - Drug pump valve (0-180 degree mapping)
NeoPixel Ring: WS2812B, 16 LEDs - RGB status indicator
Slide Switch: SPST, active LOW - Breach detection trigger
Piezo Buzzer: 5V, 2-4kHz range - Audible alerts
Push Button: Momentary, active LOW - Pain report button

---

## Workflow & Usage Demo

Once the simulation is running, act out the following scenarios to demonstrate the Agentic AI capabilities.

Scenario 1: The Homeostasis State (Normal Operation)

Action: Ensure the potentiometer is turned down and switches are off.

Observation: The OLED shows "STATUS: STABLE". The NeoPixel ring "breathes" a gentle green color. The agent is in monitoring mode.

Scenario 2: The Infection Scenario (Generative-Agentic Response)

Action: Slowly turn the Potentiometer knob to the maximum.

Observation:
- The Agent detects the bio-marker spike.
- OLED changes to "STATUS: HIGH INFECTION".
- The system simulates "GenAI Synthesizing" a custom dose.
- Actuation: The Servo motor moves (simulating drug release) and the LED ring turns solid Blue (simulating electrical stimulation).

Scenario 3: The Material Breach Scenario (Self-Healing Priority)

Action: While the infection scenario is running, flip the Slide Switch.

Observation:
- The Agent immediately interrupts the previous task (proving autonomy).
- OLED flashes "! CRITICAL FAILURE !".
- Actuation: The Servo immediately locks closed (safety first). The LED ring pulses Red and the Buzzer sounds an alarm. The system enters "Self-Healing Mode".

---

## Dependencies & Libraries

Required Libraries (Install via Wokwi Library Manager)

Library: Adafruit GFX Library
Version: 1.11.0 or higher
Purpose: Graphics primitive drawing for OLED
GitHub: https://github.com/adafruit/Adafruit-GFX-Library

Library: Adafruit SSD1306
Version: 2.5.0 or higher
Purpose: SSD1306 OLED display driver (I2C)
GitHub: https://github.com/adafruit/Adafruit_SSD1306

Library: ESP32Servo
Version: 0.11.0 or higher
Purpose: PWM servo control library
GitHub: https://github.com/RoboticsBrno/ESP32Servo

Library: Adafruit NeoPixel
Version: 1.11.0 or higher
Purpose: WS2812B RGB LED control
GitHub: https://github.com/adafruit/Adafruit_NeoPixel

Core Dependencies (Built-in)

Wire.h - I2C communication (part of Arduino core)
ESP32 HAL - Hardware abstraction layer (built into Wokwi/Arduino-ESP32)

Installation Instructions

In Wokwi: Click the "+" icon next to "Libraries" in the code editor. Search for each library name. Click "Add" next to each result. Wokwi automatically manages versions.

Locally (if using Arduino IDE): Sketch > Include Library > Manage Libraries. Search for each library name. Click "Install" for each one.

---

## How It Works

Core Philosophy: Autonomous Decision-Making at the Edge

BioSync-AI operates on a Finite State Machine (FSM) paradigm, where each "state" represents a distinct patient condition and triggers a corresponding autonomous response.

Decision Tree Logic:

1. READ SENSOR VALUES
   - Bio-Marker (Potentiometer)
   - Material Breach (Switch)
   - Patient Pain (Button)

2. DIAGNOSIS ENGINE (IF/ELSE)
   - IF breach_detected THEN -> CRITICAL FAILURE (Rank 1)
   - ELSE IF pain_reported THEN -> PAIN MANAGEMENT (Rank 2)
   - ELSE IF bio_load >= 1500 THEN -> INFECTION TREATMENT (Rank 3)
   - ELSE -> HOMEOSTASIS (Rank 4)

3. EXECUTE ACTION
   - Set LED Color
   - Set Servo Angle
   - Trigger Buzzer
   - Update Display

4. FEEDBACK (Multi-Modal UI)
   - OLED: Status & Graphs
   - RGB Ring: Color Indicator
   - Buzzer: Audio Alert
   - Servo: Drug Delivery

5. LOOP (Every 40ms)

Why This Architecture?

Zero Latency: All decisions made locally on ESP32-S3 (no cloud)
Fail-Safe: Highest-priority interrupt (Breach) always preempts
Scalable: FSM easily extended with new states
Energy Efficient: Low-power microcontroller + minimal computation
Autonomous: No human intervention required for critical responses

---

## Troubleshooting

Common Issues and Solutions

Issue 1: OLED Display Shows Nothing / Blank Screen

Possible Causes:
- Incorrect I2C address (not 0x3C)
- SDA/SCL pins swapped
- Missing Adafruit SSD1306 library

Solutions:
1. Verify I2C address by adding debug code:
   Serial.println("Scanning I2C...");
   for (uint8_t addr = 1; addr < 127; addr++) {
     Wire.beginTransmission(addr);
     if (Wire.endTransmission() == 0) {
       Serial.print("Found device at 0x");
       Serial.println(addr, HEX);
     }
   }

2. Double-check SDA=GPIO8, SCL=GPIO9 in circuit
3. Reinstall Adafruit SSD1306 from library manager

Issue 2: Servo Not Moving

Possible Causes:
- Incorrect GPIO 6 assignment
- Servo library not installed
- Power insufficient (servo draws high current)

Solutions:
1. Verify GPIO 6 is connected to servo PWM (orange wire)
2. Check servo range: 0 degrees = full close, 180 degrees = full open
3. Test with simple sweep code:
   for (int angle = 0; angle <= 180; angle += 10) {
     drugPump.write(angle);
     delay(100);
   }

Issue 3: LEDs Not Lighting / NeoPixel Dark

Possible Causes:
- Missing Adafruit NeoPixel library
- GPIO 5 disconnected
- LED ring power not supplied

Solutions:
1. Add Adafruit NeoPixel library
2. Verify GPIO 5 -> DIN (data input) on NeoPixel
3. Check 5V and GND connections to LED ring
4. Test with:
   pixels.setPixelColor(0, pixels.Color(255, 0, 0)); // Red
   pixels.show();

Issue 4: Buzzer Not Making Sound

Possible Causes:
- GPIO 10 not configured
- Buzzer polarity reversed
- tone() frequency outside range

Solutions:
1. Ensure GPIO 10 is set as OUTPUT:
   pinMode(BUZZ_PIN, OUTPUT);
   tone(BUZZ_PIN, 1000); // Test tone

2. Check buzzer connections (Positive to GPIO 10, Negative to GND)
3. Try frequency range 500-4000 Hz (typical piezo range)

Issue 5: Potentiometer Input Not Changing Display

Possible Causes:
- GPIO 4 not reading ADC
- Potentiometer not connected to 3V3 and GND
- ADC range not calibrated

Solutions:
1. Print ADC value to verify input:
   int rawBio = analogRead(POT_PIN);
   Serial.println(rawBio); // Should range 0-4095

2. Verify potentiometer connections: Left to GND, Right to 3V3, Middle to GPIO 4
3. Confirm mapping thresholds match your sensor

Issue 6: Simulation Crashes / Freezes

Possible Causes:
- Infinite loop in code
- Memory overflow
- Wokwi browser issue

Solutions:
1. Check for infinite loops in loop() function
2. Verify buffer sizes (graphBuffer[128] should fit)
3. Restart Wokwi: Refresh browser (F5)
4. Clear browser cache and try again

Debugging Tips

Enable Serial Monitor (Wokwi):
Serial.begin(115200);
Serial.println("Boot complete");
Serial.print("Bio-Load: "); Serial.println(rawBio);

Then click "Serial Monitor" in Wokwi to view output.

Add Visual Feedback:
- Change LED colors to indicate code path
- Use OLED to print variable values
- Add delays between critical sections

---

## Future Enhancements

Planned Features (Post-MVP)

Real Generative AI Integration
- Replace simulated protocol synthesis with actual LLM calls
- Use TinyML (TensorFlow Lite) for on-device model inference
- Personalized dosage based on patient history

Cloud Synchronization (Optional)
- Periodic sync to cloud database (WiFi-enabled)
- Long-term patient analytics
- Doctor dashboard for remote monitoring
- Maintain local-first autonomy for critical functions

Expanded Sensor Suite
- Real bio-impedance measurement (not potentiometer)
- Temperature sensing for infection severity
- Electrochemical sensors (glucose, lactate)
- Strain sensors for material integrity

Advanced Actuators
- Microfluidic drug delivery (replaces servo simulation)
- Controllable transdermal iontophoresis
- Electrical stimulation matrix (beyond LED indicator)

Extended Display
- Full-color ePaper display (better battery life)
- Touch interface for patient input
- Historical trend graphs (rolling 24-hour data)

Wireless Communication
- BLE (Bluetooth Low Energy) for smartphone app
- Encrypted patient data transmission
- Real-time alerts to caregiver phone

Regulatory Compliance
- FDA medical device approval pathway
- IEC 60601 electrical safety certification
- HIPAA-compliant data handling

---

## Contributors

BioSync-AI Development Team:

RunTime Slayers (Team Name)
Team members:
B.Rajendra Reddy(CB.AI.4AIM24107): Component Selection
Boddu Saran(CB.AI.U4AIM24108):GitHub preparation 
Muthuraman Ramanthan(CB.AI.U4AIM24131): Idea Improvements
K S S S Srihari Likith(CB.AI.U4AIM24152): Wokwi Simulation

Acknowledgments:
- Wokwi team for excellent ESP32 simulator
- Adafruit for robust embedded libraries

---

## Quick Links

- Wokwi Simulation: https://wokwi.com/projects/451773368870500353

## Source Code: 
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

#define SDA_PIN    8    // OLED SDA
#define SCL_PIN    9    // OLED SCL
#define POT_PIN    4    // Bio-Sensor (Potentiometer)
#define SERVO_PIN  6    // Drug Pump (Servo)
#define PIXEL_PIN  5    // LED Ring (NeoPixel)
#define BREACH_PIN 7    // Slide Switch (Tear Trigger)
#define BUZZ_PIN   10   // Piezo Buzzer
#define BTN_PIN    11   // Patient Override Button

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define NUMPIXELS     16 

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Servo drugPump;
Adafruit_NeoPixel pixels(NUMPIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

unsigned long lastPageChange = 0;
int currentPage = 0; // 0=Patient Status, 1=AI Logic, 2=Telemetry
int graphBuffer[128]; 
int bufferIdx = 0;
String patientCondition = "ANALYZING...";

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { for(;;); }
  
  drugPump.attach(SERVO_PIN); 
  pixels.begin();
  pixels.show();
  
  pinMode(BREACH_PIN, INPUT_PULLUP);
  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(BUZZ_PIN, OUTPUT);

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
  
  for(int i=0; i<128; i++) graphBuffer[i] = 45; 
}

void loop() {
  int rawBio = analogRead(POT_PIN);
  bool isBreach = !digitalRead(BREACH_PIN); // Active LOW
  bool isPain = !digitalRead(BTN_PIN);      // Active LOW

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

  int graphY = map(rawBio, 0, 4095, 63, 30); 
  graphBuffer[bufferIdx] = graphY;
  bufferIdx = (bufferIdx + 1) % 128;

  if (isBreach) {
    handleBreach();
  } else if (isPain) {
    handlePain();
  } else if (rawBio >= 1500) {
    handleTreatment(rawBio);
  } else {
    handleHomeostasis();
  }

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
