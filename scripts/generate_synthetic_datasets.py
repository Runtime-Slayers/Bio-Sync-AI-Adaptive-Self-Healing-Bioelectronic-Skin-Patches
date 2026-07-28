import numpy as np
import csv
import os

def save_csv(filename, header, col1, col2):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for c1, c2 in zip(col1, col2):
            writer.writerow([c1, c2])

def generate_datasets():
    os.makedirs('../data', exist_ok=True)
    np.random.seed(42)

    # Time array (simulating hours of monitoring instead of just seconds, scaled to 0-10 for plotting)
    # 1000 samples
    t = np.linspace(0, 10, 1000)

    # 1. Stable State (Homeostasis)
    # Baseline ~1.0 with random walk drift and sensor white noise
    drift_a = np.cumsum(np.random.normal(0, 0.015, 1000))
    noise_a = np.random.normal(0, 0.05, 1000)
    bio_a = 1.0 + drift_a + noise_a
    # Ensure it stays within bounds [0, 1.4]
    bio_a = np.clip(bio_a, 0.5, 1.4)
    save_csv('../data/stable_state.csv', ['Time(s)', 'BioSignal(a.u.)'], t, bio_a)

    # 2. Mild Inflammation
    # Starts stable, then drifts up past 1.5 (Mild threshold), then drug dosing brings it down
    drift_b = np.cumsum(np.random.normal(0, 0.02, 1000))
    noise_b = np.random.normal(0, 0.05, 1000)
    # Infection onset at t=3
    infection_curve = np.where(t > 3, 0.3 * (t - 3), 0)
    # Dosing effect starts at t=5
    dosing_effect = np.where(t > 5, -0.4 * (t - 5), 0)
    bio_b = 1.0 + drift_b + noise_b + infection_curve + dosing_effect
    bio_b = np.clip(bio_b, 0.5, 2.2)
    save_csv('../data/mild_inflammation.csv', ['Time(s)', 'BioSignal(a.u.)'], t, bio_b)

    # 3. High Infection
    # Aggressive exponential-like spike past 2.5 (Critical threshold), aggressive max dosing curbs it
    drift_c = np.cumsum(np.random.normal(0, 0.03, 1000))
    noise_c = np.random.normal(0, 0.08, 1000)
    # Infection onset at t=1, exponential growth
    infection_severe = np.where(t > 1, 0.5 * np.exp(0.5 * (t - 1)) - 0.5, 0)
    # Dosing effect starts hard at t=2
    dosing_severe = np.where(t > 2.5, -0.6 * np.exp(0.4 * (t - 2.5)) + 0.6, 0)
    bio_c = 1.0 + drift_c + noise_c + infection_severe + dosing_severe
    bio_c = np.clip(bio_c, 0.5, 3.8) # Capped by biology/sensor limit
    save_csv('../data/high_infection.csv', ['Time(s)', 'BioSignal(a.u.)'], t, bio_c)

    # 4. Servo Response (Hysteresis/Realistic Actuation)
    # BioLoad from 0 to 4095 ADC units
    bio_load = np.linspace(0, 4095, 1000)
    angle = np.zeros_like(bio_load)
    # Add non-linear actuation curve + quantization steps (servo motors move in discrete steps)
    for i, bl in enumerate(bio_load):
        if bl < 1500:
            angle[i] = 0
        elif bl < 3000:
            # Proportional with steps of 2 degrees
            raw_angle = 20 + (bl - 1500) * (120 - 20) / (3000 - 1500)
            angle[i] = np.round(raw_angle / 2.0) * 2.0
        else:
            angle[i] = 160 # Max safe angle
            
    # Add a tiny bit of jitter to simulate servo mechanical feedback noise
    angle += np.random.normal(0, 0.5, 1000)
    angle = np.clip(angle, 0, 180)
    save_csv('../data/servo_response.csv', ['BioLoad(ADC)', 'ServoAngle(deg)'], bio_load, angle)

    print("Synthetic datasets generated successfully in data/ directory.")

if __name__ == '__main__':
    generate_datasets()
