import pygame
import sys

# Color palette from your project (subtle pink/red, blue, and purple tones)
COLORS = {
    "BACKGROUND": (21, 2, 79),         # Dark purple/blue
    "TEXT": (255, 255, 255),           # White for contrast
    "USER_BOX": (199, 70, 175),        # Pinkish red
    "QC_BOX": (148, 189, 242),         # Light blue
    "OUTLINE": (185, 150, 227),        # Soft purple
    "EXIT_BTN": (199, 70, 175)         # Exit button color
}

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Factor Game")

# Fonts
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 48)

# Input box setup
user_input_box = pygame.Rect(150, 350, 200, 40)
qc_output_box = pygame.Rect(450, 350, 200, 40)
user_text = ''
active_input = False

# Exit button
exit_button = pygame.Rect(20, 20, 80, 36)

# Placeholder QC output (will update after check)
qc_text = ''

# Number to be factored
N = 15

# UI Drawing
def draw_interface():
    screen.fill(COLORS["BACKGROUND"])

    # Exit button
    pygame.draw.rect(screen, COLORS["EXIT_BTN"], exit_button)
    exit_text = FONT.render("Exit", True, COLORS["TEXT"])
    screen.blit(exit_text, (exit_button.x + 10, exit_button.y + 5))

    # Title
    title = BIG_FONT.render("Quantum Factor Game", True, COLORS["TEXT"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    # Number to be factored
    prompt = FONT.render(f"Number to be factored: {N}", True, COLORS["TEXT"])
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 120))

    # Labels
    user_label = FONT.render("User", True, COLORS["TEXT"])
    screen.blit(user_label, (user_input_box.x + 60, user_input_box.y - 40))

    qc_label = FONT.render("QC", True, COLORS["TEXT"])
    screen.blit(qc_label, (qc_output_box.x + 70, qc_output_box.y - 40))

    # Input/output boxes
    pygame.draw.rect(screen, COLORS["USER_BOX"], user_input_box, 3)
    pygame.draw.rect(screen, COLORS["QC_BOX"], qc_output_box, 3)

    # Display user input
    user_surface = FONT.render(user_text, True, COLORS["TEXT"])
    screen.blit(user_surface, (user_input_box.x + 10, user_input_box.y + 5))

    # Display QC result (if any)
    qc_surface = FONT.render(qc_text, True, COLORS["TEXT"])
    screen.blit(qc_surface, (qc_output_box.x + 10, qc_output_box.y + 5))

    # Footer instruction
    footer = FONT.render("Press Enter to check.", True, COLORS["TEXT"])
    screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    draw_interface()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Exit button check
            if exit_button.collidepoint(event.pos):
                running = False
            # Focus input box if clicked
            active_input = user_input_box.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    try:
                        user_guess = int(user_text)
                        if N % user_guess == 0:
                            qc_text = str(N // user_guess)
                        else:
                            qc_text = "Incorrect"
                    except:
                        qc_text = "Invalid"
                    user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode.isdigit():
                    user_text += event.unicode

    clock.tick(30)

pygame.quit()
sys.exit()