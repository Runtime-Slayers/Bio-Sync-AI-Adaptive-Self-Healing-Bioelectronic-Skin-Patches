import numpy as np

class FLNode:
    def __init__(self, node_id, data_size):
        self.node_id = node_id
        self.data_size = data_size
        # Simulate local model weights
        self.local_weights = np.random.randn(10)
        
    def train(self):
        # Simulate local training step (e.g. on edge patch)
        # Update weights based on local data
        self.local_weights += np.random.randn(10) * 0.1
        return self.local_weights
        
    def apply_differential_privacy(self, epsilon=0.5):
        """
        Applies Laplace noise for Differential Privacy (DP) as per paper specs.
        """
        sensitivity = 1.0 # Assumed sensitivity
        scale = sensitivity / epsilon
        noise = np.random.laplace(0, scale, self.local_weights.shape)
        return self.local_weights + noise

def federated_averaging(nodes, epsilon=0.5):
    """
    Simulates the FedAvg algorithm across multiple BioSync-AI patches.
    """
    total_data = sum([node.data_size for node in nodes])
    global_weights = np.zeros(10)
    
    for node in nodes:
        # 1. Local Training
        node.train()
        
        # 2. Apply DP before transmission
        secure_weights = node.apply_differential_privacy(epsilon)
        
        # 3. Aggregate (Weighted Average)
        weighting = node.data_size / total_data
        global_weights += secure_weights * weighting
        
    return global_weights

def main():
    print("BioSync-AI Federated Learning & Privacy Simulation (FedAvg + DP)")
    print("-" * 65)
    
    # Simulate a small cluster of wearable patches
    nodes = [FLNode(i, np.random.randint(100, 1000)) for i in range(5)]
    
    print(f"Initializing {len(nodes)} edge nodes...")
    
    # Run a few communication rounds
    for round_num in range(1, 4):
        print(f"\n--- FL Communication Round {round_num} ---")
        global_w = federated_averaging(nodes, epsilon=0.5)
        print(f"Aggregated Global Weights (first 3): {global_w[:3]}")
        
        # Broadcast back to nodes
        for node in nodes:
            node.local_weights = np.copy(global_w)
            
    print("\nSimulation complete. Differential privacy (\u03b5=0.5) applied successfully.")

if __name__ == '__main__':
    main()
