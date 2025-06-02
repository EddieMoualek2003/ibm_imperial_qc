import subprocess
import threading
import sys
import termios
import tty
import select
import time

from lights_out.lights_out_top import *
from dice_game.dice_game_top import *
from zeno_demo.zeno_demo_top import *

def run_Tie_demo():
    subprocess.run(["python3", "tie_demo_original/QuantumRaspberryTie.py"])

gameArray = [
    ["Option 1 - Lights Out", lights_out_main],
    ["Option 2 - Tie Demo", run_Tie_demo],
    ["Option 3 - Schrodinger Dice Game", dice_game_main],
    ["Option 4 - Zeno Measurement Impact", zeno_demo_main]
]

def run_with_esc_hotkey():
    stop_event = threading.Event()

    # Background thread to watch for ESC
    def esc_listener():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while not stop_event.is_set():
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                    if ch == '\x1b':  # ESC key
                        print("\n🚪 ESC key detected. Stopping...")
                        stop_event.set()
                        break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    threading.Thread(target=esc_listener, daemon=True).start()
    main_loop(stop_event)

def main_loop(stop_event):
    print("🎮 Available Quantum Demos:")
    for game in gameArray:
        print(f"\t{game[0]}")

    try:
        choice = int(input("\nEnter a game option: "))
        while not stop_event.is_set():
            gameArray[choice - 1][1]()
    except (IndexError, ValueError):
        print("❌ Invalid selection. Please enter a number from the menu.")

if __name__ == "__main__":
    run_with_esc_hotkey()
