from dice_game_functions import *
from ibm_qc_interface import *


def dice_game_main():
    # Begin by creating the quantum circuit.
    qc = createCircuit()

    # Execute the job and return the results.
    counts = quantum_execute_evolved(simulator=1, circuit=qc)
    selected = returnSelectedState(counts)
    createAnimation(selected)
    return counts

print(dice_game_main())