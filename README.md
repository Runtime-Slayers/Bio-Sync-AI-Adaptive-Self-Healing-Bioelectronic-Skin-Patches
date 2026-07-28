# BioSync-AI: Agentic AI-Driven Autonomous Bioelectronic Wearable Patch

**BioSync-AI** is a proof-of-concept bioelectronic wearable patch for real-time therapeutic intervention and predictive health management. This repository contains the code and data necessary to reproduce the hardware-in-the-loop simulation, diagnostic logic, and performance evaluations presented in our paper.

## Overview

Most commercial wearable devices perform continuous physiological monitoring and generate alerts when predefined thresholds are exceeded, but do not provide autonomous therapeutic actuation. BioSync-AI introduces a paradigm shift by performing autonomous drug delivery with edge-deployed artificial intelligence for real-time closed-loop control. 

This repository provides:
- The complete ESP32-S3 firmware (`sketch.ino`) featuring an on-device LangGraph agent dispatcher and BioBERT-Tiny inference simulation.
- Python scripts that generate synthetic biosignal data and output the performance evaluation graphs matching those shown in the paper.
- The hardware-in-the-loop safety interlock mechanisms designed to prevent drug stacking and actuate fail-closed states upon patch rupture.

## Repository Structure

```
├── README.md               # This document
├── sketch.ino              # BioSync-AI Main Control Loop (ESP32-S3 Firmware)
├── diagram.json            # Hardware schematic for Wokwi Simulation
├── libraries.txt           # Required Arduino libraries
├── scripts/                # Python scripts to generate evaluation metrics & figures
│   ├── generate_fig3.py    
│   ├── generate_fig4.py    
│   ├── generate_fig5.py    
│   └── generate_fig6.py    
├── data/                   # Output CSV data files for biosignals and performance metrics
└── figures/                # Visualizations of system performance and architecture
```

## System Architecture and Control Logic

The system is designed with four integrated layers:
1. **Physical Sensing**: Continuous biosignal acquisition simulated via analog potentiometer readings.
2. **Edge AI Inference**: Quantized BioBERT-Tiny classifying raw 128-sample buffers into distinct diagnostic states.
3. **Agentic Control (LangGraph)**: Priority-ordered state graph ensuring failsafe response mechanisms.
4. **Therapeutic Actuation & Telemetry**: Precise micro-servo transdermal valve control, NeoPixel LED status, and OLED feedback.

![Medical IoT Architecture](figures/medical_iot_flowchart.png)
![Agentic AI Control Flow](figures/iot_ai_flowchart.png)

## Evaluation Results

The agentic pipeline was thoroughly evaluated across 1000 simulated cycles. Our Python scripts (`scripts/`) systematically generate the required data and compile the visualizations representing system responsiveness and diagnostic accuracy. 

### Figure 3: Biosignal Monitoring and Drug Delivery
Shows stable homeostasis, mild inflammation, high infection transitions, and proportional valve servo control.
![Figure 3](figures/fig3_biosignal_dynamics.png)

### Figure 4: Comparative Performance Metrics
Compares BioSync-AI's anomaly detection accuracy, decision latency, and prediction confidence against consumer wearables and traditional medical pumps.
![Figure 4](figures/fig4_performance_metrics.png)

### Figure 5: Multi-Dimensional Performance Radar
Comprehensive analysis of BioSync-AI achieving full autonomous control and safety scores relative to passive wearables and reactive pumps.
![Figure 5](figures/fig5_radar_comparison.png)

### Figure 6: Latency and Power Analysis
Demonstrates a 38-fold latency reduction over cloud equivalents with minimal power consumption on-device.
![Figure 6](figures/fig6_latency_power.png)

## Getting Started

### Prerequisites

To compile the firmware, use the Arduino IDE or [Wokwi](https://wokwi.com) simulator. Ensure the following libraries are installed:
- `Adafruit_GFX`
- `Adafruit_SSD1306`
- `ESP32Servo`
- `Adafruit_NeoPixel`

To generate the figures and run the Python analytics:
```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas matplotlib
cd scripts
python generate_fig3.py
python generate_fig4.py
python generate_fig5.py
python generate_fig6.py
```
This will populate the `data/` and `figures/` directories with the corresponding `.csv` and `.png` files.

## Safety Mechanisms
BioSync-AI employs dual safety barriers:
1. **Hardware-Interlock**: The vitrimer tear-sensor overrides software, physically forcing the valve closed during structural failures.
2. **Biological-Patience Constraint**: Firmware limits consecutive dosing updates, preventing dose-stacking toxicity.

## Citation
Please refer to the manuscript for comprehensive methodological details, physiological models, and discussion on clinical implications.
