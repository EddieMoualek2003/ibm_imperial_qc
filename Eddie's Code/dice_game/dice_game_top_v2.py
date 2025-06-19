# dice_game_main.py

import argparse
from dice_game.dice_game_functions import *
from utils.ibm_qc_interface import *

# Output fallback handlers

def display_on_leds(selected):
    try:
        print("[INFO] Attempting LED output...")
        # Your LED matrix code here
        raise NotImplementedError("LEDs not available.")
    except Exception as e:
        print(f"[WARNING] LED display failed: {e}")
        return False
    return True

def display_on_emulator(selected):
    try:
        print("[INFO] Attempting Sense HAT emulator output...")
        # Emulator code here
        print("Would normally go here")
        # raise NotImplementedError("SenseHAT emulator not working.")
    except Exception as e:
        print(f"[WARNING] Emulator display failed: {e}")
        return False
    return True

def display_cli(selected):
    print(f"[CLI OUTPUT] Quantum Dice Result: {selected}")

# Main callable game logic

def dice_game_main(display_mode=None):
    """
    Run the quantum dice game with specified display output.
    :param display_mode: 'leds', 'emulator', 'cli', or None
    """
    qc = createCircuit()
    counts = ideal_simulator(qc)[0]
    selected = returnSelectedState(counts)

    if display_mode == "leds":
        if not display_on_leds(selected):
            print("[FALLBACK] Falling back to emulator.")
            if not display_on_emulator(selected):
                display_cli(selected)
    elif display_mode == "emulator":
        if not display_on_emulator(selected):
            display_cli(selected)
    else:
        display_cli(selected)

    return counts

# CLI entry point

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantum Dice Game")
    parser.add_argument(
        "--display",
        choices=["leds", "emulator", "cli"],
        help="Select output mode: leds | emulator | cli (default: cli)",
    )
    args = parser.parse_args()
    dice_game_main(display_mode=args.display)
