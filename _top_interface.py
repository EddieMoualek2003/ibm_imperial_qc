import subprocess
import threading
import keyboard

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

def run_with_hotkey():
    stop_event = threading.Event()

    # Register the hotkey
    keyboard.add_hotkey('esc', stop_event.set)

    # Start the main loop
    main_loop(stop_event)

def main_loop(stop_event):
    # Message to the user on how to leave the game
    print("Press 'ESC' to come back to the main menu when done")
    # Message to the user on the actual game modes.
    for game in gameArray:
            print(f"\t\t {game[0]}")
    # Let the user pick their game of choice
    choice = int(input("Enter a game option: "))
    # The game will be repeated until
    while not stop_event.is_set():
        # Run the game until the hot-key is pressed.
        gameArray[choice-1][1]()
        
        


# # Step 3: Main entry
# if __name__ == "__main__":
#     # debug_main()
#     for game in gameArray:
#         print(f"\t\t {game[0]}")
#     try:
#         choice = int(input("Enter a game option: "))
#         gameArray[choice-1][1]()
#     except:
#         print("Invalid Option")

# #comments