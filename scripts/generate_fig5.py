import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Data
categories = ['Accuracy', 'Response\nTime', 'Power\nEfficiency', 'Autonomous\nControl', 'Safety\nScore', 'Adaptability']
N = len(categories)

values_biosync = [0.98, 0.98, 0.90, 1.00, 1.00, 0.90]
values_fitbit = [0.60, 0.30, 0.80, 0.00, 0.20, 0.60]
values_pumps = [0.70, 0.40, 0.30, 0.70, 0.80, 0.30]

df = pd.DataFrame({
    'Dimension': categories,
    'BioSync-AI': values_biosync,
    'Fitbit/Apple': values_fitbit,
    'Med. Pumps': values_pumps
})
df.to_csv('../data/radar_comparison.csv', index=False)

# Plotting
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories)
ax.set_rlabel_position(0)
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=10)
plt.ylim(0, 1.0)

# BioSync-AI
val1 = values_biosync + values_biosync[:1]
ax.plot(angles, val1, linewidth=2, linestyle='solid', label='BioSync-AI', color='#2196F3')
ax.fill(angles, val1, '#2196F3', alpha=0.1)

# Fitbit
val2 = values_fitbit + values_fitbit[:1]
ax.plot(angles, val2, linewidth=2, linestyle='solid', label='Fitbit/Apple', color='#FF9800')
ax.fill(angles, val2, '#FF9800', alpha=0.1)

# Med Pumps
val3 = values_pumps + values_pumps[:1]
ax.plot(angles, val3, linewidth=2, linestyle='solid', label='Med. Pumps', color='#9C27B0')
ax.fill(angles, val3, '#9C27B0', alpha=0.1)

plt.title('Multi-Dimensional Performance Comparison', size=14, y=1.1, fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.tight_layout()
plt.savefig('../figures/fig5_radar_comparison.png', dpi=300)
