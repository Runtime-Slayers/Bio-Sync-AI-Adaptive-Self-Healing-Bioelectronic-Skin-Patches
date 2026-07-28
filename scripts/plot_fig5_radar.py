import matplotlib.pyplot as plt
import numpy as np
from math import pi
import csv
import os

def read_radar_csv(filepath):
    categories = []
    bio_sync = []
    fitbit = []
    pumps = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            categories.append(row[0].replace('\\n', '\n'))
            bio_sync.append(float(row[1]))
            fitbit.append(float(row[2]))
            pumps.append(float(row[3]))
    return categories, bio_sync, fitbit, pumps

def main():
    os.makedirs('../figures', exist_ok=True)
    
    # Read data
    categories, values_biosync, values_fitbit, values_pumps = read_radar_csv('../data/radar_comparison.csv')
    N = len(categories)

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
    print("Figure 5 generated successfully in figures/fig5_radar_comparison.png")

if __name__ == '__main__':
    main()
