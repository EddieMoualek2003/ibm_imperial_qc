from qiskit import QuantumCircuit
from scipy.stats import multivariate_normal
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import random

def createCircuit():
    qc = QuantumCircuit(3)
    qc.h([0, 1, 2])  # Put all qubits into superposition
    qc.measure_all()
    circuit = qc
    return circuit

def returnSelectedState(counts):
    # Use the counts dictionary from the quantum result
    # Choose one result randomly, weighted by how often it occurred
    bitstrings = list(counts.keys())
    weights = list(counts.values())
    selected = random.choices(bitstrings, weights=weights, k=1)[0]
    return selected

def createAnimation(measured_state):

    # Step 1: Define all 3-qubit basis states and their uniform probabilities
    states = ['000', '001', '010', '011', '100', '101', '110', '111']
    probabilities = [1/8] * 8  # Uniform distribution

    # Step 2: Define Gray-code-ordered 2D positions for each 3-qubit state
    state_map = {
        '000': (0, 0), '001': (0, 1), '011': (0, 2), '010': (0, 3),
        '100': (1, 0), '101': (1, 1), '111': (1, 2), '110': (1, 3)
    }

    # Step 3 (Smooth Surface): Create a smooth Gaussian at each grid cell
    x = np.linspace(-1, 4, 100)  # for q1q2
    y = np.linspace(-1, 2, 100)  # for q0
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    # Define Gaussian parameters
    sigma = 0.075  # width of each peak

    # Reinitialize Z to zero
    Z_frames = []

    # Generate interpolated Z for animation frames
    frames = 30
    for frame in range(frames):
        t = frame / (frames - 1)
        Z_frame = np.zeros_like(X)

        for state, prob in zip(states, probabilities):
            row, col = state_map[state]
            mu = [col, row]
            rv = multivariate_normal(mean=mu, cov=[[sigma, 0], [0, sigma]])
            pdf_values = rv.pdf(np.dstack((X, Y)))
            norm_factor = np.sum(pdf_values)
            bump = prob * pdf_values / norm_factor * (X.shape[0] * X.shape[1])

            if state == measured_state:
                Z_frame += (1 - t) * bump + t * (1.0 * bump / bump.sum() * (X.shape[0] * X.shape[1]))
            else:
                Z_frame += (1 - t) * bump

        Z_frames.append(Z_frame)

    # Setup the animation
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    def animate(i):
        ax.clear()
        surf = ax.plot_surface(X, Y, Z_frames[i], cmap='plasma', edgecolor='none', antialiased=True)
        ax.set_xticks(np.arange(4))
        ax.set_xticklabels(['00', '01', '11', '10'])
        ax.set_yticks(np.arange(2))
        ax.set_yticklabels(['0', '1'])
        ax.set_xlabel("q1q2 (Gray code)")
        ax.set_ylabel("q0")
        ax.set_zlabel("Smoothed |ψ|²")
        ax.set_title(f"Wavefunction Collapse to |{measured_state}⟩ ({int(measured_state, 2)}) (Frame {i+1}/{frames})")
        return [surf]

    ani = animation.FuncAnimation(fig, animate, frames=frames, interval=100, blit=False)

    plt.close()
    ani.save('resource_folder/schrodinger_dice_wavefunction_collapse.gif', writer='ffmpeg', fps=10)