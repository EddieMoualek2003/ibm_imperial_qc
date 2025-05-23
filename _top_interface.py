from lights_out_top import *
from tie_demo_top import *
from dice_game_top import *
from zeno_demo_top import *

gameArray = [
    ["Option 1 - Lights Out", lights_out_main],
    ["Option 2 - Tie Demo", tie_demo_main],
    ["Option 3 - Schrodinger Dice Game", dice_game_main],
    ["Option 4 - Zeno Measurement Impact", zeno_demo_main]
]


# Step 3: Main entry
if __name__ == "__main__":
    for game in gameArray:
        print(f"\t\t {game[0]}")
    try:
        choice = int(input("Enter a game option: "))
        gameArray[choice-1][1]()
    except:
        print("Invalid Option")
