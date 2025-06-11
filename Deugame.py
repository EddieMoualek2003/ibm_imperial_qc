import pygame
import sys
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
from qiskit_aer import AerSimulator
#hoogleboogle
# --- Pygame setup ---
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT),0)
pygame.display.set_caption("Deutsch Algorithm Interactive Demo")
font = pygame.font.SysFont("consolas", 18)
big_font = pygame.font.SysFont("consolas", 26, bold=True)
clock = pygame.time.Clock()

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (180, 100, 220) 
BLUE = (255, 105, 180)  
RED = (255, 0, 255)
GREY = (100, 100, 100)

# --- Oracle data ---
oracle_types = [
    ('constant_0', "Constant: f(x) = 0 (Always 0)"),
    ('constant_1', "Constant: f(x) = 1 (Always 1)"),
    ('balanced_identity', "Balanced: f(x) = x"),
    ('balanced_not', "Balanced: f(x) = 1 - x"),
    ('unbalanced_custom', "Unbalanced: f(0)=1, f(1)=0 (Not balanced or constant)"),
]

oracle_explanations = {
    'constant_0': "Oracle f(x) = 0: returns 0 for all inputs (constant).",
    'constant_1': "Oracle f(x) = 1: returns 1 for all inputs (constant).",
    'balanced_identity': "Oracle f(x) = x: returns input (0→0,1→1), balanced.",
    'balanced_not': "Oracle f(x) = 1 - x: negates input (0→1,1→0), balanced.",
    'unbalanced_custom': "Oracle unbalanced: flips ancilla only when input qubit = 0.\nThis is NOT constant or balanced, so Deutsch's algorithm won't classify correctly.",
}

step_texts = [
    "Initialize qubits: |q0>=|0>, |q1>=|0> (ancilla).",
    "Apply X gate to ancilla (q1) to prepare it in |1>.",
    "Apply Hadamard gates to both qubits, creating superposition.",
    "Apply the oracle (Uf) encoding function f(x).",
    "Apply Hadamard gate to input qubit (q0) again to create interference.",
    "Measure q0: 0 → constant function, 1 → balanced function."
]

info_text = (
  "Welcome to the Deutsch Algorithm Interactive Demo!\n\n"
  "The Deutsch Algorithm is a fundamental quantum algorithm that determines whether a function f(x), with a single-bit input, is\n"
  "constant (outputs the same value for every input) or balanced (outputs 0 for half the inputs and 1 for the other half), using just one evaluation.\n\n"
  "In classical computing, you need to check both possible inputs to be certain.\n"
  "This quantum algorithm leverages superposition and interference to solve this with a single query, showcasing the power of quantum computing.\n\n"
  "Press any key to proceed to the oracle selection menu.\n"
  "During the demo, press 'I' anytime to view this information screen again."
)

# --- Globals ---
qc = None
step = 0
oracle_index = 0
oracle = oracle_types[oracle_index][0]
measurement_result = None
qc_path = "circuit.png"
in_menu = False  # start with info screen first
show_info = True  # show info screen first
saved_screen = None  # To return after info screen

def init_circuit():
    global qc, step, measurement_result
    step = 0
    measurement_result = None
    qc = QuantumCircuit(2, 1)

def apply_step(n):
    global qc, measurement_result
    qc.data.clear()
    if n >= 1:
        qc.x(1)
    if n >= 2:
        qc.h(0)
        qc.h(1)
    if n >= 3:
        if oracle == 'constant_0':
            pass
        elif oracle == 'constant_1':
            qc.x(1)
        elif oracle == 'balanced_identity':
            qc.cx(0, 1)
        elif oracle == 'balanced_not':
            qc.cx(0, 1)
            qc.x(1)
        elif oracle == 'unbalanced_custom':
            qc.x(0)        # flip q0
            qc.cx(0, 1)     # flip ancilla if q0=1 (original q0=0)
            qc.x(0)        # restore q0
    if n >= 4:
        qc.h(0)
    if n >= 5:
        qc.measure(0, 0)
        sim = AerSimulator()
        result = sim.run(qc, shots=1024).result()
        counts = result.get_counts()
        measurement_result = max(counts, key=counts.get)

def save_circuit_image():
    circuit_drawer(qc, output="mpl", filename=qc_path)
    plt.close()

# New multiline text drawer: splits on \n and optionally wraps long lines
def draw_multiline_text(surface, text, x, y, font, color=WHITE, wrap_width=None, line_height=None):
    lines = text.split('\n')
    if line_height is None:
        line_height = font.get_height() + 4
    y_offset = 0
    for line in lines:
        if wrap_width is not None:
            # Word wrap for the line
            words = line.split(' ')
            wrapped_line = ""
            for word in words:
                test_line = wrapped_line + word + " "
                if font.size(test_line)[0] <= wrap_width:
                    wrapped_line = test_line
                else:
                    # Render the wrapped line and move to next line
                    text_surface = font.render(wrapped_line, True, color)
                    surface.blit(text_surface, (x, y + y_offset))
                    y_offset += line_height
                    wrapped_line = word + " "
            # Render remainder of the wrapped line
            if wrapped_line:
                text_surface = font.render(wrapped_line, True, color)
                surface.blit(text_surface, (x, y + y_offset))
                y_offset += line_height
        else:
            # No wrapping, just render the line
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (x, y + y_offset))
            y_offset += line_height

def draw_info_screen():
    screen.fill(BLACK)
    draw_multiline_text(screen, "Deutsch Algorithm Info", 50, 20, big_font, GREEN)

    # Define a box for info text
    info_box_rect = pygame.Rect(50, 80, 1100, 600)  # width 1100, height 600 px max
    pygame.draw.rect(screen, (30, 30, 30), info_box_rect, border_radius=8)  # dark background box

    # Draw the info text inside this box with wrapping
    draw_multiline_text(screen, info_text, info_box_rect.x + 10, info_box_rect.y + 10, font, WHITE, wrap_width=info_box_rect.width - 20)

    # Draw the bottom instruction text
    draw_multiline_text(screen, "Press any key to continue.", 50, 700, font, BLUE)
    pygame.display.flip()


def draw_menu():
    screen.fill(BLACK)
    draw_multiline_text(screen, "Select Oracle Function (Use UP/DOWN arrows and ENTER):", 50, 100, big_font, GREEN)
    for i, (_, desc) in enumerate(oracle_types):
        color = BLUE if i == oracle_index else WHITE
        draw_multiline_text(screen, desc, 100, 160 + i*40, big_font, color)
    pygame.display.flip()

def draw_demo():
    screen.fill(BLACK)
    # Title
    draw_multiline_text(screen, "Deutsch Algorithm Interactive Demo", 30, 20, big_font, GREEN)

    # Oracle info box
    oracle_box = pygame.Rect(30, 70, 560, 140)
    pygame.draw.rect(screen, GREY, oracle_box, border_radius=8)
    pygame.draw.rect(screen, BLUE, oracle_box, 3, border_radius=8)
    draw_multiline_text(screen, f"Oracle: {oracle_types[oracle_index][1]}", 40, 75, big_font, BLUE)
    draw_multiline_text(screen, oracle_explanations[oracle], 40, 110, font, WHITE, wrap_width=520)

    # Step explanation box
    step_box = pygame.Rect(30, 220, 560, 80)
    pygame.draw.rect(screen, GREY, step_box, border_radius=8)
    pygame.draw.rect(screen, BLUE, step_box, 3, border_radius=8)
    draw_multiline_text(screen, f"Step {step}: ", 40, 225, big_font, BLUE)
    draw_multiline_text(screen, step_texts[step], 40, 255, font, WHITE, wrap_width=520)

    # Controls
    controls_y = 320
    draw_multiline_text(screen, "Controls:", 40, controls_y, big_font, BLUE)
    draw_multiline_text(screen, "← Previous Step  → Next Step  ESC Back to Menu\n" "  I Show Info  Q Quit", 40, controls_y + 35, font, WHITE)

    # Measurement result
    if measurement_result is not None:
        result_msg = f"Measurement Result: {measurement_result} → "
        if measurement_result == '0':
            result_msg += "Function is CONSTANT"
            color = GREEN
        else:
            result_msg += "Function is BALANCED"
            color = RED
        draw_multiline_text(screen, result_msg, 40, controls_y + 80, font, color)

    # Circuit image on right
    save_circuit_image()
    circuit_img = pygame.image.load(qc_path)
    circuit_img = pygame.transform.smoothscale(circuit_img, (600, 460))
    screen.blit(circuit_img, (610, 70))

    # Deutsch Algorithm overview box
    algo_box = pygame.Rect(30, 420, 560, 380)
    pygame.draw.rect(screen, GREY, algo_box, border_radius=8)
    pygame.draw.rect(screen, BLUE, algo_box, 3, border_radius=8)
    draw_multiline_text(screen, "Deutsch Algorithm Overview:", 40, 430, big_font, BLUE)
    algo_text = (
        "This quantum algorithm determines if a function f(x) is constant or balanced with a single query.\n\n"
        "Key ideas:\n"
        "- Initialize qubits\n"
        "- Create superposition\n"
        "- Apply oracle that flips ancilla conditioned on f(x)\n"
        "- Apply interference via Hadamard\n"
        "- Measure input qubit\n\n"
        "If measurement is 0, f(x) is constant; if 1, f(x) is balanced.\n"
        "Unbalanced oracles break the assumptions, so results are unreliable."
    )
    draw_multiline_text(screen, algo_text, 40, 470, font, WHITE, wrap_width=520)

    pygame.display.flip()

# --- Main program ---
def run_deutsch_game():
    global qc, step, oracle_index, oracle, measurement_result, in_menu, show_info

    init_circuit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if show_info:
                    if in_menu:
                        show_info = False
                    else:
                        show_info = False
                        in_menu = True
                else:
                    if in_menu:
                        if event.key == pygame.K_UP:
                            oracle_index = (oracle_index - 1) % len(oracle_types)
                            oracle = oracle_types[oracle_index][0]
                        elif event.key == pygame.K_DOWN:
                            oracle_index = (oracle_index + 1) % len(oracle_types)
                            oracle = oracle_types[oracle_index][0]
                        elif event.key == pygame.K_RETURN:
                            in_menu = False
                            step = 0
                            measurement_result = None
                            init_circuit()
                            apply_step(step)
                        elif event.key == pygame.K_i:
                            show_info = True
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    else:
                        if event.key == pygame.K_RIGHT:
                            if step < 5:
                                step += 1
                                apply_step(step)
                        elif event.key == pygame.K_LEFT:
                            if step > 0:
                                step -= 1
                                apply_step(step)
                        elif event.key == pygame.K_ESCAPE:
                            in_menu = True
                            step = 0
                            measurement_result = None
                        elif event.key == pygame.K_i:
                            show_info = True
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

        if show_info:
            draw_info_screen()
        elif in_menu:
            draw_menu()
        else:
            draw_demo()

        clock.tick(30)

if __name__ == "__main__":
    run_deutsch_game()