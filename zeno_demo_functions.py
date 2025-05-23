from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from math import *
import pickle

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
        fig.savefig(f"resource_folder/zeno_quantum_circuit{i}.png")

    return [probabilities, [row[1] for row in factorArray]]

def write_pickle(zeno_qc_structure, numOperators, backend = "simulator"):
    with open(f"resource_folder/quantum_zeno_data_num_op{numOperators}_{backend}.pkl", "wb") as f:
        pickle.dump(zeno_qc_structure, f)