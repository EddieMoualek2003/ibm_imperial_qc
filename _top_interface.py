import subprocess
import threading
import time
from pynput import keyboard as pynput_keyboard

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

    # Start the ESC key listener in a separate thread
    def on_press(key):
        if key == pynput_keyboard.Key.esc:
            print("Key Press Detected")
            stop_event.set()
            return False  # Stop the listener

    listener = pynput_keyboard.Listener(on_press=on_press)
    listener.start()

    # Run the main loop (blocks until stop_event is set)
    main_loop(stop_event)

    # Wait for listener to finish before exiting
    listener.join()

def main_loop(stop_event):
    print("Press 'ESC' to come back to the main menu when done")
    for game in gameArray:
        print(f"\t\t {game[0]}")
    choice = int(input("Enter a game option: "))

    while not stop_event.is_set():
        gameArray[choice-1][1]()

if __name__ == "__main__":
    run_with_hotkey()
