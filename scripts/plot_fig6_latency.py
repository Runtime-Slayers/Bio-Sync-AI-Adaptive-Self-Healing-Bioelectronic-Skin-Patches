import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def read_data(filepath):
    names, vals = [], []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            names.append(row[0].replace('\\n', '\n'))
            vals.append(float(row[1]))
    return names, vals

def main():
    os.makedirs('../figures', exist_ok=True)
    
    systems_lat, latency = read_data('../data/latency_comparison.csv')
    systems_pow, power = read_data('../data/power_comparison.csv')

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # (a) Latency
    y_pos = np.arange(len(systems_lat))
    axs[0].barh(y_pos, latency, align='center', color=['#2196F3', '#FF9800', '#9C27B0', '#F44336'])
    axs[0].set_yticks(y_pos)
    axs[0].set_yticklabels(systems_lat)
    axs[0].invert_yaxis()  # labels read top-to-bottom
    axs[0].set_xlabel('Response Latency (ms)')
    axs[0].set_title('(a) Therapeutic Response Latency', fontweight='bold')
    axs[0].set_xscale('log')

    for i, v in enumerate(latency):
        axs[0].text(v + (v * 0.1), i, f'{v}ms', va='center')

    # (b) Power
    colors = ['#2196F3', '#9C27B0', '#FF9800']
    explode = (0.1, 0, 0)
    axs[1].pie(power, explode=explode, labels=systems_pow, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=140)
    axs[1].axis('equal')
    axs[1].set_title('(b) Relative Power Consumption (W)', fontweight='bold')

    plt.tight_layout()
    plt.savefig('../figures/fig6_latency_power.png', dpi=300)
    print("Figure 6 generated successfully in figures/fig6_latency_power.png")

if __name__ == '__main__':
    main()
