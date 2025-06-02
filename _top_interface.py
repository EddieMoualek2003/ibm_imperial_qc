import subprocess
import threading
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

def debug_main():
    choice = int(input("Enter a game option: "))
    gameArray[choice-1][1]()

def run_with_quit_input():
    stop_event = threading.Event()

    # Launch a background thread to listen for ENTER key
    def wait_for_enter():
        input("\n📎 Press ENTER at any time to stop and return to the main menu...\n")
        stop_event.set()

    threading.Thread(target=wait_for_enter, daemon=True).start()

    # Run the game menu loop
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
    run_with_quit_input()
