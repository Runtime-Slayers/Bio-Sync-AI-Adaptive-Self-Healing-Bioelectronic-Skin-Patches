import numpy as np
import matplotlib.pyplot as plt
import csv
import os

def read_csv(filepath):
    x, y = [], []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return np.array(x), np.array(y)

def main():
    os.makedirs('../figures', exist_ok=True)

    # Read data
    t_a, bio_a = read_csv('../data/stable_state.csv')
    t_b, bio_b = read_csv('../data/mild_inflammation.csv')
    t_c, bio_c = read_csv('../data/high_infection.csv')
    bio_load, angle = read_csv('../data/servo_response.csv')

    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))

    # (a) Stable
    axs[0, 0].plot(t_a, bio_a, color='tab:green')
    axs[0, 0].axhline(y=1.5, color='orange', linestyle='--', alpha=0.7, label='Mild threshold')
    axs[0, 0].axhline(y=2.5, color='red', linestyle='--', alpha=0.7, label='Critical threshold')
    axs[0, 0].set_title('(a) Stable / Normal State')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_ylabel('Bio-Signal (a.u.)')
    axs[0, 0].set_ylim(-1, 4)
    axs[0, 0].legend()
    axs[0, 0].grid(True, alpha=0.3)

    # (b) Mild Inflammation
    axs[0, 1].plot(t_b, bio_b, color='tab:blue')
    axs[0, 1].axhline(y=1.5, color='orange', linestyle='--', alpha=0.7)
    axs[0, 1].axhline(y=2.5, color='red', linestyle='--', alpha=0.7)
    axs[0, 1].fill_between(t_b, -1, 4, where=(t_b > 5), color='orange', alpha=0.1, label='Drug dosing active')
    axs[0, 1].set_title('(b) Mild Inflammation + Agentic Dosing')
    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_ylabel('Bio-Signal (a.u.)')
    axs[0, 1].set_ylim(-1, 4)
    axs[0, 1].legend()
    axs[0, 1].grid(True, alpha=0.3)

    # (c) High Infection
    axs[1, 0].plot(t_c, bio_c, color='tab:red')
    axs[1, 0].axhline(y=1.5, color='orange', linestyle='--', alpha=0.7)
    axs[1, 0].axhline(y=2.5, color='red', linestyle='--', alpha=0.7)
    axs[1, 0].fill_between(t_c, -1, 5, color='red', alpha=0.1, label='Max-dose active')
    axs[1, 0].set_title('(c) High Infection: Max Therapeutic Response')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_ylabel('Bio-Signal (a.u.)')
    axs[1, 0].set_ylim(-1, 5)
    axs[1, 0].legend()
    axs[1, 0].grid(True, alpha=0.3)

    # (d) Servo Angle
    axs[1, 1].plot(bio_load, angle, color='purple', linewidth=2)
    axs[1, 1].axvline(x=1500, color='orange', linestyle='--', alpha=0.7, label='Mild onset')
    axs[1, 1].axvline(x=3000, color='red', linestyle='--', alpha=0.7, label='Severe onset')
    axs[1, 1].set_title('(d) Drug Pump: Servo Angle vs. Bio-Load')
    axs[1, 1].set_xlabel('Bio-Load (ADC units, 0--4095)')
    axs[1, 1].set_ylabel('Servo Angle (°)')
    axs[1, 1].legend()
    axs[1, 1].grid(True, alpha=0.3)

    plt.suptitle('BioSync-AI Real-Time Biosignal Monitoring and Therapeutic Response', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../figures/fig3_biosignal_dynamics.png', dpi=300)
    print("Figure 3 generated successfully in figures/fig3_biosignal_dynamics.png")

if __name__ == '__main__':
    main()
