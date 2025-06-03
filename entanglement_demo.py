from qiskit import QuantumCircuit
import time
from utils.ibm_qc_interface import noisy_simulator  
from sense_emu import SenseHat

def speak(message):
    print(f"\n🗣️ {message}")

def get_user_input():
    user_text = input("Please enter your guess for Qubit B (0 or 1): ").strip()
    if '1' in user_text:
        return '1'
    elif '0' in user_text:
        return '0'
    else:
        return None

def display_on_hat(hat, qubit_a, qubit_b):
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    OFF = [0, 0, 0]
    pixels = [OFF[:] for _ in range(64)]

    # Display qubit A in top left 2x2 and qubit B in top right 2x2
    color_a = GREEN if qubit_a == '1' else RED
    color_b = GREEN if qubit_b == '1' else RED
    for i in [0, 1, 8, 9]:
        pixels[i] = color_a
    for i in [6, 7, 14, 15]:
        pixels[i] = color_b

    hat.set_pixels(pixels)

# Game setup
hat = SenseHat()
hat.clear()
score = 0
rounds = 5

speak("Welcome to the Quantum Entanglement Time Challenge!")
time.sleep(2)

for i in range(rounds):
    speak(f"Round {i+1}. Preparing entangled qubits...")

    # Create entangled circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    # Simulate
    counts = noisy_simulator(qc)
    outcome = list(counts.keys())[0] 
    qubit_b, qubit_a = outcome[0], outcome[1]

    display_on_hat(hat, qubit_a, '0')  # Display Qubit A only
    speak(f"Qubit A is measured as {qubit_a}. Make your prediction for Qubit B (0 or 1).")

    prediction = get_user_input()

    if prediction is None:
        speak(f"No valid input detected. Qubit B was {qubit_b}.")
    elif prediction == qubit_b:
        speak("Correct! As expected from perfect entanglement, Qubit B matches Qubit A.")
        score += 1
    else:
        speak(f"Incorrect. Qubit B was actually {qubit_b}.")

    display_on_hat(hat, qubit_a, qubit_b)
    time.sleep(1.5)
    hat.clear()

speak(f"Game over. You scored {score} out of {rounds}. Well done!")

# Cleanup
hat.clear()
