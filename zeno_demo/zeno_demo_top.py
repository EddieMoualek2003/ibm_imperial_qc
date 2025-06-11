import numpy as np
import matplotlib.pyplot as plt
from utils.ibm_qc_interface import *
from zeno_demo.zeno_demo_functions import *


def process_circuit(numOpPerStage, noisy=False):
    probabilityArray = []
    circuit = create_circuit(numOpPerStage, theta=pi/2) # Create the circuit with the number of operators and theta value
    print("Circuit Created")
    if noisy:
        print("Noisy Simulator Mode")
        # Run the circuit on the noisy simulator
        s1, shots = noisy_simulator(circuit)
    else:
        print("Ideal Simulator Mode")
        # Run the circuit on the ideal simulator
        s1, shots = ideal_simulator(circuit)
    numZero = list(s1.values())[list(s1.keys()).index('0')] # Find the occurence of 0
    p = numZero/shots # Calculate the probability of measuring the zero state
    return s1, circuit, probabilityArray, p


def zeno_demo_main(numOperators = 4):
    # Everything will be run on the simulator, so set this to True.
    simulator = True
    probabilityGroup = []
    circuitGroup = []
    factorArray = returnFactors(numOperators)
    for factorPair in factorArray:
        numOpPerStage = factorPair[0]
        numIter = factorPair[1]
        for i in range(numIter): # Repeat for all the iterations needed
            print(f">>> # Operators: {numOperators}, # Iterations: {numIter}, Current Iteration: {i + 1}")
            s1, circuit, probabilityArray = process_circuit(numOpPerStage=numOpPerStage, noisy=simulator)

            numZero = list(s1.values())[list(s1.keys()).index('0')] # Find the occurence of 0
            p = numZero/4096
            print(f"Probability of Zero State is {p}")
            if i < numIter - 1:
                if p > 0.5: # This means the state has not changed from the 0 state yet.
                    probabilityArray.append(p)
                else: # This means the system has changed state
                    probabilityArray.append(1-p)
                    break
            elif i == numIter-1:
                probabilityArray.append(1-p)
                break
            print(probabilityArray)
        circuitGroup.append(circuit)
        probabilityGroup.append(probabilityArray)
    zeno_qc_structure = {
        "QC"    :   circuitGroup, 
        "P"     :   probabilityGroup,
        "dim"   :   factorArray
    }
    [x, y] = zeno_data_analysis(zeno_qc_structure)

    # Create the figure and plot
    fig, ax = plt.subplots()
    ax.scatter(y, x)
    ax.set_title("Probability of State Change")
    ax.set_xlabel("Number of Measurements")
    ax.set_ylabel("Probability of State Change (Time Evolution)")
    ax.set_xlim(0, int(numOperators)+2)
    ax.set_ylim(0, 1)

    # Save the figure
    backend = "simulator" if simulator else "QC"
    plt.savefig(f"resource_folder/zeno_probability_plot_numOp{numOperators}_{backend}.png", dpi=300, bbox_inches='tight')

    # Optional: display the plot
    # plt.show()

    write_pickle(zeno_qc_structure=zeno_qc_structure, numOperators=numOperators, backend=backend)  

    return zeno_qc_structure

# print(zeno_demo_main(int(input("Number of Operators: "))))
