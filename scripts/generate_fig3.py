import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create directories
os.makedirs('../data', exist_ok=True)
os.makedirs('../figures', exist_ok=True)

# Generate data for Fig 3
np.random.seed(42)

# (a) Stable
t_a = np.linspace(0, 10, 1000)
bio_a = 1.0 + 0.8 * np.sin(2 * np.pi * 1.5 * t_a) + 0.2 * np.random.randn(1000)
bio_a = np.clip(bio_a, 0, 2.2)

# (b) Mild Inflammation
t_b = np.linspace(0, 10, 1000)
# starts stable, goes up at t=5
baseline_b = 1.0 + (t_b > 5) * 1.0
bio_b = baseline_b + 0.8 * np.sin(2 * np.pi * 1.5 * t_b) + 0.2 * np.random.randn(1000)

# (c) High Infection
t_c = np.linspace(0, 10, 1000)
bio_c = 3.5 + 0.4 * np.sin(2 * np.pi * 3.0 * t_c) + 0.3 * np.random.randn(1000)

# (d) Servo Angle
bio_load = np.linspace(0, 4095, 1000)
angle = np.zeros_like(bio_load)
for i, bl in enumerate(bio_load):
    if bl >= 1500:
        angle[i] = 20 + (bl - 1500) * (160 - 20) / (4095 - 1500)

# Save to CSV
pd.DataFrame({'Time': t_a, 'BioSignal': bio_a}).to_csv('../data/stable_state.csv', index=False)
pd.DataFrame({'Time': t_b, 'BioSignal': bio_b}).to_csv('../data/mild_inflammation.csv', index=False)
pd.DataFrame({'Time': t_c, 'BioSignal': bio_c}).to_csv('../data/high_infection.csv', index=False)
pd.DataFrame({'BioLoad': bio_load, 'ServoAngle': angle}).to_csv('../data/servo_response.csv', index=False)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(14, 8))

# a
axs[0, 0].plot(t_a, bio_a, color='tab:green')
axs[0, 0].axhline(y=1.5, color='orange', linestyle='--', alpha=0.7, label='Mild threshold')
axs[0, 0].axhline(y=2.5, color='red', linestyle='--', alpha=0.7, label='Critical threshold')
axs[0, 0].set_title('(a) Stable / Normal State')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Bio-Signal (a.u.)')
axs[0, 0].set_ylim(-1, 4)
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.3)

# b
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

# c
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

# d
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
