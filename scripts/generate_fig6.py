import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data
df_latency = pd.DataFrame({
    'System': ['BioSync-AI\n(On-Edge)', 'Cloud-Based\nWearable', 'Traditional\nMed Pump', 'Manual\nHospital'],
    'Latency (ms)': [8.4, 320, 480, 3600]
})
df_latency.to_csv('../data/latency_comparison.csv', index=False)

df_power = pd.DataFrame({
    'System': ['BioSync-AI (15W peak)', 'NVIDIA Jetson Xavier (30W)', 'Cloud-Based System (85W)'],
    'Power (W)': [15, 30, 85]
})
df_power.to_csv('../data/power_comparison.csv', index=False)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# (a) Latency
y_pos = np.arange(len(df_latency['System']))
axs[0].barh(y_pos, df_latency['Latency (ms)'], align='center', color=['#2196F3', '#FF9800', '#9C27B0', '#F44336'])
axs[0].set_yticks(y_pos)
axs[0].set_yticklabels(df_latency['System'])
axs[0].invert_yaxis()  # labels read top-to-bottom
axs[0].set_xlabel('Response Latency (ms)')
axs[0].set_title('(a) Therapeutic Response Latency', fontweight='bold')
axs[0].set_xscale('log')

for i, v in enumerate(df_latency['Latency (ms)']):
    axs[0].text(v + (v * 0.1), i, f'{v}ms', va='center')

# (b) Power
colors = ['#2196F3', '#9C27B0', '#FF9800']
explode = (0.1, 0, 0)
axs[1].pie(df_power['Power (W)'], explode=explode, labels=df_power['System'], colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=140)
axs[1].axis('equal')
axs[1].set_title('(b) Relative Power Consumption (W)', fontweight='bold')

plt.tight_layout()
plt.savefig('../figures/fig6_latency_power.png', dpi=300)
