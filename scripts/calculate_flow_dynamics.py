import numpy as np
import matplotlib.pyplot as plt
import os

# Physical constants from paper modeling
# Equations (6) and (7)
theta_max = 180  # Max servo angle
A_max = 2.0  # Max valve cross-sectional area (mm^2)
delta_P = 5.0  # Micropump diff pressure (kPa)
mu_fluid = 2.0  # Drug solution viscosity (mPa*s)
L_channel = 10.0 # Microchannel length (mm)

# We compute flow rate Q_drug(theta) for angles from 0 to 180
angles = np.linspace(0, 180, 500)

# Equation (6): A_valve(theta) = A_max * sin^2((pi * theta) / (2 * theta_max))
A_valve = A_max * np.sin((np.pi * angles) / (2 * theta_max))**2

# Equation (7): Q_drug(theta) = (delta_P * A_valve^2) / (8 * pi * mu_fluid * L_channel)
# Note: This is a proportional representation, converting units appropriately would scale Q.
Q_drug = (delta_P * A_valve**2) / (8 * np.pi * mu_fluid * L_channel)

def main():
    os.makedirs('../figures', exist_ok=True)
    
    fig, ax1 = plt.subplots(figsize=(8, 6))

    color = 'tab:red'
    ax1.set_xlabel('Servo Angle (Degrees)')
    ax1.set_ylabel('Valve Area $A_{valve}$ (mm$^2$)', color=color)
    ax1.plot(angles, A_valve, color=color, linewidth=2, label='Valve Area')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Flow Rate $Q_{drug}$ (a.u.)', color=color)
    ax2.plot(angles, Q_drug, color=color, linewidth=2, linestyle='--', label='Flow Rate')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Hagen-Poiseuille Microfluidic Flow Dynamics vs Servo Angle')
    plt.grid(True, alpha=0.3)
    plt.savefig('../figures/flow_dynamics.png', dpi=300)
    print("Flow dynamics computed and plot saved to figures/flow_dynamics.png")

if __name__ == '__main__':
    main()
