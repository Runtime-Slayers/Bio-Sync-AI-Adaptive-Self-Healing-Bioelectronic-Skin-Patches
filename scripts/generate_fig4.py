import matplotlib.pyplot as plt
import numpy as np
import csv

# Data
metrics = ['Anomaly Det. Accuracy (%)', 'Detection Latency (ms)', 'Drug Dose Accuracy (%)', 'Prediction Confidence (%)']
bio_sync = [98.4, 8.4, 97.2, 98.4]
fitbit = [62.0, 320.0, 0.0, 55.0]
pumps = [70.0, 480.0, 78.0, 68.0]

with open('../data/performance_comparison.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Metric', 'BioSync-AI', 'Fitbit/Apple Watch', 'Traditional Med. Pumps'])
    for m, b, fb, p in zip(metrics, bio_sync, fitbit, pumps):
        writer.writerow([m, b, fb, p])

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(metrics))
width = 0.25

rects1 = ax.bar(x - width, bio_sync, width, label='BioSync-AI', color='#2196F3')
rects2 = ax.bar(x, fitbit, width, label='Fitbit/Apple Watch', color='#FF9800')
rects3 = ax.bar(x + width, pumps, width, label='Traditional Med. Pumps', color='#9C27B0')

ax.set_ylabel('Performance Value', fontsize=12)
ax.set_title('BioSync-AI vs. Existing Systems: Key Performance Metrics', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10)
ax.legend()
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
