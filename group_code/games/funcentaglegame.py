def run_quantum_match():
    import pygame
    import random
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    pygame.init()

    WIDTH, HEIGHT = 900, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quantum Match - Entanglement Demo")

    FONT = pygame.font.SysFont("Arial", 24)
    BIG_FONT = pygame.font.SysFont("Arial", 36)

    GRAY, BLACK, PINK, GREEN, RED, YELLOW, WHITE = (200, 200, 200), (0, 0, 0), (255, 46, 210), (0, 200, 0), (200, 0, 0), (255, 255, 0), (255, 255, 255)

    INSTRUCTIONS, DEMO_MODE, PLAYER_SELECT, PLAY_MODE, END_SCREEN = "instructions", "demo", "player_select", "play", "end"
    state = INSTRUCTIONS
    message = ""
    game_mode = None
    scores = {"Player 1": 0, "Player 2": 0, "Computer": 0}
    current_player = "Player 1"

    class Qubit:
        SIZE = 100

        def __init__(self, id, x, y):
            self.id = id
            self.rect = pygame.Rect(x, y, Qubit.SIZE, Qubit.SIZE)
            self.state = "superposition"
            self.entangled_with = None
            self.measured = False
            self.animation_timer = 0

        def measure(self):
            if not self.measured:
                result = random.choice(["0", "1"])
                self.state = result
                self.measured = True
                self.animation_timer = pygame.time.get_ticks()
                if self.entangled_with and not self.entangled_with.measured:
                    self.entangled_with.state = result
                    self.entangled_with.measured = True
                    self.entangled_with.animation_timer = pygame.time.get_ticks()

        def draw(self, screen):
            color = GRAY
            if self.state == "superposition":
                color = PINK
            elif self.state == "0":
                color = RED
            elif self.state == "1":
                color = GREEN

            elapsed = pygame.time.get_ticks() - self.animation_timer
            if self.measured and elapsed < 300:
                pygame.draw.rect(screen, YELLOW, self.rect.inflate(20, 20))
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

            label = FONT.render(f"Q{self.id}", True, BLACK)
            screen.blit(label, (self.rect.x + 30, self.rect.y + 35))

    def draw_instructions():
        SCREEN.fill(WHITE)
        title = BIG_FONT.render("Quantum Match - Learn How to Play", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
        lines = [
            "Superposition: Qubits are both 0 and 1 until measured!",
            "Entanglement: Measure one, and its partner collapses too!",
            "Goal: Find matching pairs — some are entangled, some not.",
            "",
            "Click to continue to the demo..."
        ]
        for i, line in enumerate(lines):
            text = FONT.render(line, True, BLACK)
            SCREEN.blit(text, (50, 120 + i * 40))

    def draw_demo():
        SCREEN.fill(WHITE)
        title = BIG_FONT.render("Entanglement Demo", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        for q in demo_qubits:
            q.draw(SCREEN)
        if current_demo_step < len(demo_instructions):
            lines = demo_instructions[current_demo_step].split('\n')
            for i, line in enumerate(lines):
                text = FONT.render(line, True, BLACK)
                SCREEN.blit(text, (50, 450 + i * 30))
        else:
            msg_surface = FONT.render(message, True, BLACK)
            SCREEN.blit(msg_surface, (50, 500))

    def draw_player_select():
        SCREEN.fill(WHITE)
        title = BIG_FONT.render("Select Game Mode", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        SCREEN.blit(FONT.render("Press 1 for Two Players", True, BLACK), (WIDTH // 2 - 120, 250))
        SCREEN.blit(FONT.render("Press 2 to Play Against Computer", True, BLACK), (WIDTH // 2 - 160, 300))

    def draw_play_mode():
        SCREEN.fill(WHITE)
        title = BIG_FONT.render("Play Mode", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        opponent = "Player 2" if game_mode == "2players" else "Computer"
        score_text = f"Player 1: {scores['Player 1']}    {opponent}: {scores[opponent]}"
        SCREEN.blit(FONT.render(score_text, True, BLACK), (WIDTH // 2 - 150, 70))
        SCREEN.blit(FONT.render(f"Turn: {current_player}", True, RED), (WIDTH // 2 - 60, 100))
        for q in qubits:
            q.draw(SCREEN)

    def draw_winner_screen():
        SCREEN.fill(WHITE)
        title = BIG_FONT.render("Game Over!", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        opponent = "Player 2" if game_mode == "2players" else "Computer"
        msg = "It's a tie!" if scores["Player 1"] == scores[opponent] else f"{'Player 1' if scores['Player 1'] > scores[opponent] else opponent} wins!"
        SCREEN.blit(FONT.render(msg, True, RED), (WIDTH // 2 - 80, 200))
        SCREEN.blit(FONT.render("Click anywhere to play again", True, BLACK), (WIDTH // 2 - 150, 300))

    demo_qubits = []
    positions = [(100 + (i % 3) * 100, 150 + (i // 3) * 120) for i in range(6)]
    for i, pos in enumerate(positions):
        demo_qubits.append(Qubit(i, pos[0], pos[1]))
    demo_qubits[0].entangled_with = demo_qubits[1]
    demo_qubits[1].entangled_with = demo_qubits[0]
    demo_qubits[4].entangled_with = demo_qubits[5]
    demo_qubits[5].entangled_with = demo_qubits[4]
    demo_steps = [(0, 1, True), (2, 3, False)]
    current_demo_step = 0
    demo_instructions = [
        "Step 1: Click Q0 to measure it.\nIt is entangled with Q1, so both will collapse to the same result and you get a point!",
        "Step 2: Click Q2 to measure it.\nQ2 is NOT entangled with any qubit, so only Q2 collapses.\nThen click Q3 to measure it separately.\nBoth behave independently since they are not entangled."
    ]
    clicked_ids = []
    qubits = []

    def handle_demo_click(qid):
        nonlocal current_demo_step, message, state
        if current_demo_step >= len(demo_steps): return
        step = demo_steps[current_demo_step]
        valid_ids, entangled = step[:2], step[2]
        if qid in valid_ids:
            q = demo_qubits[qid]
            if not q.measured:
                q.measure()
                clicked_ids.append(qid)
                if entangled and q.entangled_with:
                    q.entangled_with.measure()
                    clicked_ids.clear()
                    message = f"Great! Q{q.id} and Q{q.entangled_with.id} matched because they are entangled."
                    current_demo_step += 1
                elif not entangled and len(clicked_ids) == 2:
                    message = f"Q{clicked_ids[0]} and Q{clicked_ids[1]} collapsed independently."
                    clicked_ids.clear()
                    draw_demo()
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    current_demo_step += 1

    def create_qubits_with_qiskit():
        nonlocal qubits
        qubits = []
        rows, cols = 4, 7
        for i in range(rows * cols):
            x = 50 + (i % cols) * 110
            y = 130 + (i // cols) * 110
            qubits.append(Qubit(i, x, y))

        num_qubits = len(qubits)
        available_indices = list(range(num_qubits))
        random.shuffle(available_indices)

        qc = QuantumCircuit(num_qubits)
        while len(available_indices) >= 2:
            q1, q2 = available_indices.pop(), available_indices.pop()
            if random.random() < 0.5:
                qc.h(q1)
                qc.cx(q1, q2)
                qubits[q1].entangled_with = qubits[q2]
                qubits[q2].entangled_with = qubits[q1]
        qc.measure_all()
        sim = AerSimulator()
        sim.run(qc).result()

    running = True
    clock = pygame.time.Clock()
    computer_thinking = False
    computer_wait_start = None
    computer_wait_time = 1000

    while running:
        if state == INSTRUCTIONS:
            draw_instructions()
        elif state == DEMO_MODE:
            draw_demo()
        elif state == PLAYER_SELECT:
            draw_player_select()
        elif state == PLAY_MODE:
            draw_play_mode()
            if game_mode == "computer" and current_player == "Computer":
                if not computer_thinking:
                    computer_wait_start = pygame.time.get_ticks()
                    computer_thinking = True
                elif pygame.time.get_ticks() - computer_wait_start >= computer_wait_time:
                    unmeasured = [q for q in qubits if not q.measured]
                    if unmeasured:
                        q = random.choice(unmeasured)
                        q.measure()
                        if q.entangled_with and q.entangled_with.measured and q.state == q.entangled_with.state:
                            scores["Computer"] += 1
                    current_player = "Player 1"
                    computer_thinking = False
                    if all(q.measured for q in qubits):
                        state = END_SCREEN
        elif state == END_SCREEN:
            draw_winner_screen()

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == INSTRUCTIONS:
                    state = DEMO_MODE
                elif state == DEMO_MODE:
                    for i, q in enumerate(demo_qubits):
                        if q.rect.collidepoint(event.pos):
                            handle_demo_click(i)
                            break
                    if current_demo_step >= len(demo_steps):
                        state = PLAYER_SELECT
                elif state == END_SCREEN:
                    state = PLAYER_SELECT
                elif state == PLAY_MODE:
                    if (game_mode == "2players" and current_player in ["Player 1", "Player 2"]) or (game_mode == "computer" and current_player == "Player 1"):
                        for q in qubits:
                            if q.rect.collidepoint(event.pos) and not q.measured:
                                q.measure()
                                if q.entangled_with and q.entangled_with.measured and q.state == q.entangled_with.state:
                                    scores[current_player] += 1
                                current_player = (
                                    "Computer" if game_mode == "computer" and current_player == "Player 1"
                                    else "Player 2" if current_player == "Player 1"
                                    else "Player 1"
                                )
                                if all(q.measured for q in qubits):
                                    state = END_SCREEN
                                break
            elif event.type == pygame.KEYDOWN and state == PLAYER_SELECT:
                if event.key == pygame.K_1:
                    game_mode = "2players"
                    scores = {"Player 1": 0, "Player 2": 0}
                    current_player = "Player 1"
                    create_qubits_with_qiskit()
                    message = ""
                    state = PLAY_MODE
                elif event.key == pygame.K_2:
                    game_mode = "computer"
                    scores = {"Player 1": 0, "Computer": 0}
                    current_player = "Player 1"
                    create_qubits_with_qiskit()
                    message = ""
                    state = PLAY_MODE

    pygame.quit()
run_quantum_match()
