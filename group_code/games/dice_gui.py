import pygame
import sys
import os
from PIL import Image, ImageSequence
from utils.dice_game_functions import dice_game_main

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schroedinger's Dice Game")

# --- Colors and Fonts ---
COLORS = {
    "BACKGROUND": (233, 206, 255),
    "TEXT": (26, 0, 71),
    "INPUT_BOX": (199, 70, 175),
    "BUTTON": (148, 189, 242),
    "BUTTON_TEXT": (26, 0, 71),
    "INPUT_TEXT": (255, 255, 255),
    "EXIT_BTN": (177, 193, 254),
    "FIGURE_BOX": (255, 255, 255)
}
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 48)

# --- UI Rectangles ---
input_box = pygame.Rect(300, 250, 200, 40)
simulate_button = pygame.Rect(320, 320, 160, 50)
exit_button = pygame.Rect(20, 20, 80, 36)
figure_box = pygame.Rect(600, 150, 360, 320)

# --- State ---
user_input = ''
active_input = False
message = "Enter number of measurements (1–100):"
FIGURE_PATH = "resource_folder/schrodinger_dice_wavefunction_collapse.gif"

# --- Animation ---
gif_frames = []
gif_frame_index = 0
gif_last_update = 0
gif_frame_delay = 100  # ms per frame


def draw_interface():
    global gif_frame_index, gif_last_update
    screen.fill(COLORS["BACKGROUND"])

    # Exit button
    pygame.draw.rect(screen, COLORS["EXIT_BTN"], exit_button, border_radius=10)
    screen.blit(FONT.render("Exit", True, COLORS["TEXT"]), (exit_button.x + 10, exit_button.y + 5))

    # Title
    screen.blit(BIG_FONT.render("Schrodinger's Dice", True, COLORS["TEXT"]), (WIDTH // 2 - 100, 40))

    # Instruction
    screen.blit(FONT.render(message, True, COLORS["TEXT"]), (100, 140))

    # Roll button
    pygame.draw.rect(screen, COLORS["BUTTON"], simulate_button, border_radius=10)
    screen.blit(FONT.render("Roll", True, COLORS["BUTTON_TEXT"]), (simulate_button.x + 40, simulate_button.y + 10))

    # Simulation Output Label
    screen.blit(FONT.render("Simulation Output", True, COLORS["TEXT"]), (figure_box.x + 50, figure_box.y - 35))
    pygame.draw.rect(screen, COLORS["FIGURE_BOX"], figure_box, border_radius=15)
    pygame.draw.rect(screen, COLORS["TEXT"], figure_box, 2, border_radius=15)

    # Animated GIF Playback
    if gif_frames:
        current_time = pygame.time.get_ticks()
        if current_time - gif_last_update > gif_frame_delay:
            gif_frame_index = (gif_frame_index + 1) % len(gif_frames)
            gif_last_update = current_time
        frame = gif_frames[gif_frame_index]
        scaled = pygame.transform.smoothscale(frame, (figure_box.width, figure_box.height))
        screen.blit(scaled, (figure_box.x, figure_box.y))

    pygame.display.flip()


# --- Main Loop ---
clock = pygame.time.Clock()
running = True
while running:
    draw_interface()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active_input = True
            else:
                active_input = False

            if simulate_button.collidepoint(event.pos):
                try:
                    dice_game_main()  # generate new GIF
                    if os.path.exists(FIGURE_PATH):
                        gif_frames.clear()
                        pil_img = Image.open(FIGURE_PATH)
                        for frame in ImageSequence.Iterator(pil_img):
                            frame = frame.convert("RGBA")
                            pg_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                            gif_frames.append(pg_frame)
                        gif_frame_index = 0
                        gif_last_update = pygame.time.get_ticks()
                        print(f"Loaded {len(gif_frames)} frames from GIF.")
                    else:
                        print("GIF not found at:", FIGURE_PATH)
                except Exception as e:
                    print("Error running simulation:", e)

            if exit_button.collidepoint(event.pos):
                running = False

        elif event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.unicode.isdigit():
                user_input += event.unicode

    clock.tick(30)

pygame.quit()
sys.exit()
