import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data
data = {
    'Metric': ['Anomaly Det. Accuracy (%)', 'Detection Latency (ms)', 'Drug Dose Accuracy (%)', 'Prediction Confidence (%)'],
    'BioSync-AI': [98.4, 8.4, 97.2, 98.4],
    'Fitbit/Apple Watch': [62.0, 320.0, 0.0, 55.0],
    'Traditional Med. Pumps': [70.0, 480.0, 78.0, 68.0]
}
df = pd.DataFrame(data)
df.to_csv('../data/performance_comparison.csv', index=False)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(df['Metric']))
width = 0.25

rects1 = ax.bar(x - width, df['BioSync-AI'], width, label='BioSync-AI', color='#2196F3')
rects2 = ax.bar(x, df['Fitbit/Apple Watch'], width, label='Fitbit/Apple Watch', color='#FF9800')
rects3 = ax.bar(x + width, df['Traditional Med. Pumps'], width, label='Traditional Med. Pumps', color='#9C27B0')

ax.set_ylabel('Performance Value', fontsize=12)
ax.set_title('BioSync-AI vs. Existing Systems: Key Performance Metrics', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df['Metric'], fontsize=10)
ax.legend()

# Set Detection Latency bar limits differently if needed or use log scale for latency visualization
# To match the paper, latency is shown on a logarithmic scale visually or capped.
# We will just plot values directly, but cap latency at 120 visually for comparison,
# or add labels on top of the bars to be clear.
ax.set_ylim(0, 110)

def autolabel(rects):
    """Attach a text label above each bar."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, min(height, 100)),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, color=rect.get_facecolor())

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('../figures/fig4_performance_metrics.png', dpi=300)
