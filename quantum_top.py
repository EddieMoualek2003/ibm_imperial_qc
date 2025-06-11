from shor_reb import shor_reb_main
from quantum_factor.quantum_factor_top import *
from funcentaglegame import *
gameArray = [
    ["Shor's Game - Rebecca", shor_reb_main],
    ["Shor's Game - Eddie", quantum_factor_game],
    ["Quantum Entanglement Match - Sophie", run_quantum_match]
    # ["Tie Demo", run_Tie_demo],
    # ["Schrodinger Dice Game", dice_game_main],
    # ["Zeno Measurement Impact", zeno_demo_main]
]

def debug_main():
    for i, option in enumerate(gameArray):
        print(f"Option {i+1} - {gameArray[i][0]}")

    choice = int(input("Enter a game option: "))
    gameArray[choice-1][1]()

if __name__ == "__main__":
    # shor_reb_main()
    debug_main()