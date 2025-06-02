import subprocess

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



# Step 3: Main entry
if __name__ == "__main__":
    # debug_main()
    for game in gameArray:
        print(f"\t\t {game[0]}")
    try:
        choice = int(input("Enter a game option: "))
        gameArray[choice-1][1]()
    except:
        print("Invalid Option")

#comments