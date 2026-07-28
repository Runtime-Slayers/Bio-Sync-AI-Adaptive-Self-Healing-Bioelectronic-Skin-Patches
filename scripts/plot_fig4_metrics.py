import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def read_metrics_csv(filepath):
    metrics = []
    bio_sync = []
    fitbit = []
    pumps = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            metrics.append(row[0])
            bio_sync.append(float(row[1]))
            fitbit.append(float(row[2]))
            pumps.append(float(row[3]))
    return metrics, bio_sync, fitbit, pumps

def main():
    os.makedirs('../figures', exist_ok=True)
    
    # Read data
    metrics, bio_sync, fitbit, pumps = read_metrics_csv('../data/performance_comparison.csv')

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
    print("Figure 4 generated successfully in figures/fig4_performance_metrics.png")

if __name__ == '__main__':
    main()
