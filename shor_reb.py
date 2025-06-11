import pygame 
import sys
import math
import random
from math import log2

from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer 
from fractions import Fraction
from collections import Counter
import numpy as np
from math import ceil, gcd
from qiskit.circuit.library import UnitaryGate
from ibm_qc_interface import *


### Pygame setup
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Period Hunter – Factor Quest")
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

BLACK = (255, 255, 255) #white
WHITE = (21, 2, 79) # dark blue
RED = (199, 70, 175) # pink
GREEN = (70, 171, 199) # light blue
BLUE = (148, 189, 242)
YELLOW = (185, 150, 227)

BUTTON_WIDTH = 60
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
BUTTON_Y = 150


### pygame functions
def generate_sequence(a, N, max_length=30):
    vals = []
    val = 1
    for x in range(max_length):
        val = (val * a) % N
        vals.append(val)
        if val == 1 and x != 0:
            break
    return vals

def draw_sequence(seq, show_hint=False, period=None):
    if not seq:
        return
    bar_width = WIDTH // len(seq)
    max_val = max(seq) if seq else 1
    for i, val in enumerate(seq):
        height = (val / max_val) * 300 + 20
        color = BLUE
        if show_hint and period and i >= period:
            color = YELLOW
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - height - 150, bar_width - 2, height))

def calculate_factors(a, r, N):
    if r % 2 != 0:
        return None, None
    val = pow(a, r // 2, N)
    factor1 = math.gcd(val - 1, N)
    factor2 = math.gcd(val + 1, N)
    if factor1 in [1, N] or factor2 in [1, N]:
        return None, None
    return factor1, factor2

def new_problem():
    semiprimes = [(15, 2), (21, 2), (35, 3), (33, 2)] #, (55, 2), (77, 3)
    while True:
        N, a = random.choice(semiprimes)
        print (f"New problem: N={N}, a={a}")
        seq = generate_sequence(a, N)
        period = len(seq)
        factors = calculate_factors(a, period, N)
        if factors != (None, None):
            return N, a, seq

def render_centered_text(text, y, color=WHITE):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)

def render_multiline_text(lines, start_y, line_height=30, color=WHITE):
    for i, line in enumerate(lines):
        render_centered_text(line, start_y + i * line_height, color)

def draw_prime_buttons(prime_options, selected_factors):
    total_width = len(prime_options) * (BUTTON_WIDTH + BUTTON_MARGIN) - BUTTON_MARGIN
    start_x = (WIDTH - total_width) // 2
    buttons = []
    for i, p in enumerate(prime_options):
        x = start_x + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        rect = pygame.Rect(x, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        color = GREEN if p in selected_factors else BLUE
        pygame.draw.rect(screen, color, rect)
        text_surf = font.render(str(p), True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        buttons.append((rect, p))
    return buttons

def run_fake_shor(N):
    for a in range(2, N):
        r_seq = generate_sequence(a, N)
        r = len(r_seq)
        factors = calculate_factors(a, r, N)
        if factors != (None, None):
            return factors
    return None


### Qiskit functions
# create a unitary gate for modular multiplication
def mod_mul_gate_unitary(a: int, N: int, m_target: int) -> UnitaryGate:
    dim = 2 ** m_target
    U = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y < N:
            U[(a * y) % N, y] = 1.0
        else:
            U[y, y] = 1.0

    return UnitaryGate(U, label=f"mult_{a}_mod_{N}")

# create a quantum circuit for Shor's algorithm
def create_quantum_circuit(n_count, m_target, a, N):
    qc = QuantumCircuit(n_count + m_target, n_count)
    qc.h(range(n_count))                  # Hadamard on counting qubits
    qc.x(n_count)                         # |1⟩ state in target register

    for q in range(n_count):
        power = pow(a, 2 ** q, N)
        mod_gate = mod_mul_gate_unitary(power, N, m_target).control()
        qc.append(mod_gate, [q] + list(range(n_count, n_count + m_target)))

    # Apply inverse QFT
    qc.append(QFT(n_count, inverse=True, do_swaps=True).to_gate(label="QFT†"), range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc

def measure(qc):
    sim = Aer.get_backend('statevector_simulator') #AerSimulator()
    tqc = transpile(qc, sim)
    result = sim.run(tqc).result()
    return result.get_counts()

# Convert the result counts to a cleaned format
def result_clean_convert(counts):
    cleaned_counts = Counter()
    for bitstring, count in counts.items():
        bits = bitstring.split(' ')[0]
        cleaned_counts[int(bits, 2)] += count
    return cleaned_counts

def estimate_period(measured_value, n_count, N):
    phase = (measured_value) / (2**n_count)
    frac = Fraction(phase).limit_denominator(N)
    print(f"Phase ≈ {phase}, Approximated as {frac}, period r = {frac.denominator}")
    return frac.denominator

# math to find factors of N using the period r
def find_factors(frequency, n_count, N, a):
    for value, _ in frequency.most_common(5):
        r = estimate_period(value, n_count, N)
        if r % 2 == 0 and pow(a, r, N) == 1:
            x = pow(a, r // 2, N)
            factors = [gcd(x - 1, N), gcd(x + 1, N), r] 
            # for f in factors:
            #     if f not in [1, N]:
            #         return f
            if factors[0] not in [1, N] and factors[1] not in [1, N]:
                print (f"Found period r={r}")
                return factors
    return None, None

# Run the quantum circuit and return the frequency of measured values
def run_quantum_circuit(n_count, m_target, a, N):
    qc = create_quantum_circuit(n_count, m_target, a, N)
    print("Circuit Created")
    counts = measure(qc)
    print("Circuit Measured", counts)
    frequency = result_clean_convert(counts)
    print("Frequency Recorded: ", frequency)
    return frequency


### Main game loop
def main():
    intro_number = 3315
    intro_factors = [3, 5]
    prime_options = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    selected_factors = set()

    N, a, base_sequence = None, None, None
    period = None
    repeats = None
    sequence = None

    guess = ""
    result_text = ""
    show_hint = False
    factors = (None, None)
    user_factor1 = ""
    user_factor2 = ""
    factor_input_stage = 1

    phase = "intro_factor_select"

    clock = pygame.time.Clock()
    running = True

    instructions = [
        "Type numbers and press Enter to submit.",
        "Press 'H' to toggle hint showing cycle repetition.",
        "Press 'R' to restart with a new problem.",
        "Press 'Q' to factor with simulated Shor.",
        "Backspace to delete digits.",
        "Press 'X' to leave the game."
    ]

    buttons = []

    while running:
        screen.fill(BLACK)

        if phase == "intro_factor_select":
            render_centered_text(f"Try to find the prime factors of N = {intro_number}", 80, YELLOW)
            render_centered_text("Select prime factors by clicking the buttons below:", 120, WHITE)
            buttons = draw_prime_buttons(prime_options, selected_factors)
            render_centered_text("Press Enter when done, or 'S' to skip.", 210)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        elif phase == "intro_shor_explain":
            explanation_lines = [
               "Awesome! Now let's explore how quantum ideas help us factor numbers.",
                "You'll see a sequence made by computing a^x mod N.",
                "Your goal is to find the period of it.",
                "This mimics what a quantum computer does in Shor's algorithm!",
                "Press Enter to begin the quest."
            ]
            render_multiline_text(explanation_lines, 130, 35, YELLOW)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        elif phase == "guess_period":
            if sequence:
                draw_sequence(sequence, show_hint, period if show_hint else None)
            for i, line in enumerate(instructions):
                instr_surf = small_font.render(line, True, WHITE)
                screen.blit(instr_surf, (20, HEIGHT - 140 + i * 25))
            render_centered_text("Guess the period of the sequence:", 40)
            render_centered_text("Enter the period and press Enter: " + guess, 80)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        elif phase == "show_formula":
            formula_lines = [
                f"Good job! You found the period r = {period}",
                "From r and a, calculate factors using:",
                "factor1 = gcd(a^(r/2) - 1, N)",
                "factor2 = gcd(a^(r/2) + 1, N)",
                "Press Enter to continue."
            ]
            render_multiline_text(formula_lines, 110, 35, GREEN)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        elif phase == "choose_factor_input":
            choose_lines = [
                "Do you want to guess the factors yourself?",
                "Type 'Y' for yes or 'N' to see the factors."
            ]
            render_multiline_text(choose_lines, 130, 35, YELLOW)

        elif phase == "input_factors":
            prompt = "Enter factor 1: " if factor_input_stage == 1 else "Enter factor 2: "
            current_input = user_factor1 if factor_input_stage == 1 else user_factor2
            render_centered_text(prompt + current_input, 150)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        elif phase == "show_factors":
            render_centered_text("Factors found:", 110, GREEN)
            render_centered_text(f"{factors[0]} and {factors[1]}", 150, GREEN)
            render_centered_text("Now reconstruct N by multiplying factors.", 190)
            render_centered_text("Enter N and press Enter: " + guess, 230)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        elif phase == "completed":
            render_centered_text("Congratulations! You reconstructed N correctly!", 150, GREEN)
            render_centered_text(f"N = {factors[0]} * {factors[1]} = {N}", 190, GREEN)
            render_centered_text("Press R to try a new problem.", 230)
            if result_text:
                color = GREEN if "correct" in result_text.lower() else RED
                render_centered_text(result_text, HEIGHT - 180, color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if phase == "intro_factor_select":
                    mouse_pos = event.pos
                    for rect, p in buttons:
                        if rect.collidepoint(mouse_pos):
                            if p in selected_factors:
                                selected_factors.remove(p)
                            else:
                                selected_factors.add(p)
                            break

            elif event.type == pygame.KEYDOWN:
                if phase == "intro_factor_select":
                    if event.key == pygame.K_RETURN:
                        if selected_factors == set(intro_factors):
                            phase = "intro_shor_explain"
                            result_text = ""
                        else:
                            result_text = "Not all factors correct yet, try again or press 'S' to skip."
                    elif event.unicode.lower() == 's':
                        phase = "intro_shor_explain"
                        result_text = ""

                elif phase == "intro_shor_explain":
                    if event.key == pygame.K_RETURN:
                        N, a, base_sequence = new_problem()
                        period = len(base_sequence)
                        repeats = random.randint(2, 5)
                        sequence = base_sequence * repeats

                        guess = ""
                        result_text = ""
                        show_hint = False
                        factors = (None, None)
                        user_factor1 = ""
                        user_factor2 = ""
                        factor_input_stage = 1

                        phase = "guess_period"

                elif phase == "guess_period":
                    if event.key == pygame.K_RETURN:
                        if guess.isdigit():
                            val = int(guess)
                            if val == period:
                                result_text = "Correct! Period found."
                                factors = calculate_factors(a, period, N)
                                if factors == (None, None):
                                    result_text = "Factors could not be found for this period."
                                phase = "show_formula"
                            else:
                                result_text = "Wrong period, try again."
                        else:
                            result_text = "Please enter a valid number."
                        guess = ""
                    elif event.key == pygame.K_x:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        guess = guess[:-1]
                    elif event.unicode.isdigit():
                        if len(guess) < 10:
                            guess += event.unicode

                elif phase == "show_formula":
                    if event.key == pygame.K_RETURN:
                        if factors != (None, None):
                            phase = "choose_factor_input"
                            result_text = ""
                        else:
                            result_text = "No factors available."

                elif phase == "choose_factor_input":
                    if event.unicode.lower() == 'y':
                        user_factor1 = ""
                        user_factor2 = ""
                        factor_input_stage = 1
                        phase = "input_factors"
                        result_text = "Enter factor 1."
                    elif event.unicode.lower() == 'n':
                        phase = "show_factors"
                        result_text = ""

                elif phase == "input_factors":
                    current_input = user_factor1 if factor_input_stage == 1 else user_factor2
                    if event.key == pygame.K_RETURN:
                        if current_input.isdigit():
                            val = int(current_input)
                            if factor_input_stage == 1:
                                user_factor1 = current_input
                                factor_input_stage = 2
                                result_text = "Enter factor 2."
                            else:
                                user_factor2 = current_input
                                guessed_factors = (int(user_factor1), int(user_factor2))
                                correct_set = {factors[0], factors[1]}
                                guessed_set = {guessed_factors[0], guessed_factors[1]}
                                if guessed_set == correct_set:
                                    result_text = "Great! You guessed the factors correctly."
                                else:
                                    result_text = "Your factors were incorrect."
                                phase = "show_factors"
                        else:
                            result_text = "Please enter a valid number."
                        if factor_input_stage == 1:
                            user_factor1 = ""
                        else:
                            user_factor2 = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if factor_input_stage == 1:
                            user_factor1 = user_factor1[:-1]
                        else:
                            user_factor2 = user_factor2[:-1]
                    elif event.unicode.isdigit():
                        if factor_input_stage == 1 and len(user_factor1) < 10:
                            user_factor1 += event.unicode
                        elif factor_input_stage == 2 and len(user_factor2) < 10:
                            user_factor2 += event.unicode

                elif phase == "show_factors":
                    if event.key == pygame.K_RETURN:
                        if guess.isdigit():
                            val = int(guess)
                            if val == factors[0] * factors[1]:
                                phase = "completed"
                                result_text = "Correct!"
                            else:
                                result_text = "Incorrect product, try again."
                            guess = ""
                        else:
                            result_text = "Please enter a valid number."
                            guess = ""
                    elif event.key == pygame.K_BACKSPACE:
                        guess = guess[:-1]
                    elif event.unicode.isdigit():
                        if len(guess) < 15:
                            guess += event.unicode

                elif phase == "completed":
                    if event.key == pygame.K_r:
                        N, a, base_sequence = new_problem()
                        period = len(base_sequence)
                        repeats = random.randint(2, 5)
                        sequence = base_sequence * repeats
                        guess = ""
                        result_text = ""
                        show_hint = False
                        factors = (None, None)
                        phase = "intro_factor_select"
                        user_factor1 = ""
                        user_factor2 = ""
                        factor_input_stage = 1
                        selected_factors = set()

                if event.key == pygame.K_h and phase not in ["intro_factor_select", "intro_shor_explain", "show_formula", "completed"]:
                    show_hint = not show_hint

                if event.key == pygame.K_r and phase not in ["intro_factor_select", "intro_shor_explain", "completed"]:
                    N, a, base_sequence = new_problem()
                    period = len(base_sequence)
                    repeats = random.randint(2, 5)
                    sequence = base_sequence * repeats
                    guess = ""
                    result_text = ""
                    show_hint = False
                    factors = (None, None)
                    phase = "guess_period"


                if event.key == pygame.K_q:
                    print(a)
                    print(N)
                    m_target = ceil(log2(N))
                    n_count = ceil(log2(N**2))
                    

                    frequency = run_quantum_circuit(n_count, m_target, a, N)

                    if not frequency:
                        result_text = "Quantum simulation failed to find a usable period."
                    else:
                        measured_value, _ = frequency.most_common(1)[0]
                        print(f"Measured value: {measured_value}")
                        r = estimate_period(measured_value, n_count, N=N)
                        print(f"Estimated period r: {r}")

                        if r and r > 0:
                            factors = find_factors(frequency, n_count, N, a) #calculate_factors(a, r, N)
                            r = factors[2] if factors else r
                            print(f"Qiskit found period r={r}, factors: {factors[0]}, {factors[1]}")
                            if factors != (None, None):
                                result_text = f"Qiskit found period r={r}, factors: {factors[0]}, {factors[1]}" #period was r
                                phase = "show_factors"
                            else:
                                result_text = f"Period r={r} did not yield nontrivial factors." #period was r
                        else:
                            result_text = "Failed to estimate a valid period."

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()