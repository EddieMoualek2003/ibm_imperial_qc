from tie_demo_functions import *  # Assumed to include load_qasm
from tie_demo_sensehat import *
import time
import numpy as np
from sense_emu import SenseHat

def main():
    hat = SenseHat()
    gameMode = 1
    while True:
        if not gameMode:
            while True:
                layout = input("How would you like to display the result: ").upper()
                bitstring = rank_scores()
                print(bitstring)
                num_states = len(bitstring)
                print(f"The state with the highest occurrence out of {num_states} states is {bitstring[-1][0]}")
                time_delay_array = computeDelay(num_states, 5).tolist()
                for i, element in enumerate(bitstring):
                    # display_bitstring_on_sensehat(hat = hat, bitstring=element[0])
                    display_bitstring_on_sensehat(hat = hat, bitstring=element[0], layout=layout)
                    time.sleep(time_delay_array[i])
                print("Next Computation will begin in:")
                time_delay = 5
                for i in range(time_delay):
                    timeLeft = time_delay-i
                    word = "second" if timeLeft == 1 else "seconds"
                    print(f"\t\t{timeLeft} {word}.")
                    time.sleep(1)
        else:
            print("Super secret mode entered. Well Bloody Done.")
            overrideCircuit()
            gameMode = 0
            print("Now get out...")

if __name__ == "__main__":
    main()

