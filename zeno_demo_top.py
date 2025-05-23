from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import ibm_qc_interface
from math import sqrt
import numpy as np
import pickle

def zeno_top(backend, numOperators):
    probabilityGroup = []
    circuitGroup = []
    factorArray = returnFactors(numOperators)
    for factorPair in factorArray:
        numOpPerStage = factorPair[0]
        numIter = factorPair[1]
        for i in range(numIter): # Repeat for all the iterations needed
            print(f">>> # Operators: {numOperators}, # Iterations: {numIter}, Current Iteration: {i + 1}")
            probabilityArray = []
            circuit = simulatedMeasurement(numOpPerStage, 0.2)
            print("Circuit Created")
            isa_circuit = ibm_qc_interface.transpilation(circuit=circuit, backend=backend)
            print("Circuit Transpiled")
            sampler = ibm_qc_interface.runSampler(backend=backend)
            print("Circuit Queued")
            s1 = ibm_qc_interface.runJob(isa_circuit, sampler).data.meas.get_counts()
            print("Job Executed")
            # s1 = multi_measure_output.data.meas.get_counts()
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
        circuitGroup.append(circuit)
        probabilityGroup.append(probabilityArray)
    zeno_qc_structure = {
        "QC"    :   circuitGroup, 
        "P"     :   probabilityGroup,
        "dim"   :   factorArray
    }

    with open(f"quantum_zeno_data_num_op{numOperators}.pkl", "wb") as f:
        pickle.dump(zeno_qc_structure, f)

    return zeno_qc_structure

## This function is responsible for returning pairs that will be used to place measurements after certain numbers of operations
def returnFactors(numOperators):
    factors = []
    for i in range(1,numOperators+1):
        if numOperators%i == 0:
            factors.append(i)
    factorPairs = []
    
    for i in range(int(len(factors)/2)):
        factorPairs.append([factors[i], factors[len(factors)-1-i]])
        factorPairs.append([factors[len(factors)-1-i], factors[i]])

    if len(factors)%2 != 0:
        factorPairs.append([int(sqrt(numOperators)), int(sqrt(numOperators))])
    return factorPairs


def simulatedMeasurement(numOperators, theta):
    qc1 = QuantumCircuit(1, 1)
    for i in range(numOperators):
        qc1.ry(theta, 0)
    qc1.measure_all()
    return qc1


def zeno_data_analysis(xeno_qc_structure):
    # Access the dictionary contents properly
    circuits = xeno_qc_structure['QC']
    probabilities = xeno_qc_structure['P']
    factorArray = xeno_qc_structure['dim']

    for i, circuit in enumerate(circuits):
        fig = circuit.draw("mpl")
        fig.savefig(f"quantum_circuit{i}.png")

    return [probabilities, [row[1] for row in factorArray]]