import pygame
import sys
import random
import time
from utils.shor_func import shor_func, shor_func_mod

# Color palette
COLORS = {
    "BACKGROUND": (233, 206, 255),
    "TEXT": (26, 0, 71),
    "USER_BOX": (199, 70, 175),
    "QC_BOX": (148, 189, 242),
    "OUTLINE": (185, 150, 227),
    "EXIT_BTN": (177, 193, 254),
    "CORRECT": (170, 255, 170),
    "WRONG": (255, 170, 170)
}

# Init PyGame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Factor Game")

# Fonts
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 48)

# Elements
user_input_box = pygame.Rect(150, 350, 200, 40)
qc_output_box = pygame.Rect(450, 350, 200, 40)
exit_button = pygame.Rect(20, 20, 80, 36)

# State
user_text = ''
qc_text = ''
footer_text = "Press Enter to check."
active_input = False
N = 7

def update_num():
    return random.randint(2, 20)

user_box_color = COLORS["USER_BOX"]
qc_box_color = COLORS["QC_BOX"]  # ✅ New color state for QC box

def draw_interface():
    screen.fill(COLORS["BACKGROUND"])

    # Exit button
    pygame.draw.rect(screen, COLORS["EXIT_BTN"], exit_button, border_radius=10)
    exit_text = FONT.render("Exit", True, COLORS["TEXT"])
    screen.blit(exit_text, (exit_button.x + 10, exit_button.y + 5))

    # Title and prompt
    title = BIG_FONT.render("Quantum Factor Game", True, COLORS["TEXT"])
    prompt = FONT.render(f"Number to be factored: {N}", True, COLORS["TEXT"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 120))

    # Tries left
    tries_left_text = FONT.render(f"Tries left: {triesLimit - triesCount}", True, COLORS["TEXT"])
    screen.blit(tries_left_text, (WIDTH // 2 - tries_left_text.get_width() // 2, 160))

    # Labels
    screen.blit(FONT.render("User", True, COLORS["TEXT"]), (user_input_box.x + 60, user_input_box.y - 40))
    screen.blit(FONT.render("QC", True, COLORS["TEXT"]), (qc_output_box.x + 70, qc_output_box.y - 40))

    # Input boxes with dynamic color
    pygame.draw.rect(screen, user_box_color, user_input_box, border_radius=10)
    pygame.draw.rect(screen, qc_box_color, qc_output_box, border_radius=10)

    # Input/output text
    screen.blit(FONT.render(user_text, True, COLORS["TEXT"]), (user_input_box.x + 10, user_input_box.y + 5))
    screen.blit(FONT.render(qc_text, True, COLORS["TEXT"]), (qc_output_box.x + 10, qc_output_box.y + 5))

    # Footer
    screen.blit(FONT.render(footer_text, True, COLORS["TEXT"]), (WIDTH // 2 - 100, HEIGHT - 50))

    pygame.display.flip()

triesLimit = 5
triesCount = 0
solved = False
# Main loop
clock = pygame.time.Clock()
running = True
while running:
    draw_interface()

    if triesCount == triesLimit or solved:
        N = update_num()
        triesCount = 0
        solved = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.collidepoint(event.pos):
                running = False
            active_input = user_input_box.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    try:
                        user_guess = int(user_text)
                        if N % user_guess == 0:
                            user_box_color = COLORS["CORRECT"]
                            footer_text = "Correct. You win!"
                            qc_box_color = COLORS["QC_BOX"]  # reset to default
                            solved = True

                        else:
                            user_box_color = COLORS["WRONG"]
                            footer_text = "Incorrect. Quantum Computer's Turn."
                            stop = False
                            while not stop:
                                a = random.randint(2, N-1)
                                print(f"Current value of a: {a}")
                                factor, frequency = shor_func_mod(N, a)
                                if factor == "ncp":
                                    print("NCP Detected")
                                    continue
                                else:
                                    print("Co prime a used - Moving forward.")
                                    stop = True
                            if factor == 0:
                                qc_box_color = COLORS["WRONG"]
                                triesCount += 1 # Only increment the number of tries if 
                                footer_text = "The quantum computer failed this round."
                            else:
                                qc_box_color = COLORS["CORRECT"]
                                footer_text = "The quantum computer wins!"
                                solved = True
                                qc_text = str(factor)
                            # print("Factor found is:", factor)
                        if triesCount == triesLimit:
                            footer_text = "Niether of you solved it. Changing the problem."

                    except ValueError:
                        user_box_color = COLORS["WRONG"]
                        qc_box_color = COLORS["WRONG"]
                        qc_text = "Invalid"
                        footer_text = "Please enter a number."

                    draw_interface()
                    pygame.display.flip()
                    pygame.time.delay(2000)

                    # Reset UI
                    user_text = ''
                    user_box_color = COLORS["USER_BOX"]
                    qc_box_color = COLORS["QC_BOX"]
                    footer_text = "Press Enter to check."
                    qc_text = ''

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                    user_box_color = COLORS["USER_BOX"]
                    footer_text = "Press Enter to check."

                elif event.unicode.isdigit():
                    user_text += event.unicode
                    user_box_color = COLORS["USER_BOX"]
                    footer_text = "Press Enter to check."

    clock.tick(30)

pygame.quit()
sys.exit()
