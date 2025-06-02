from qiskit import QuantumCircuit
import qiskit.qasm3
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.visualization import circuit_drawer
from utils.ibm_qc_interface import *

def load_qasm(filename):
    return qiskit.qasm3.load(filename)

def overrideCircuit():
    qc = QuantumCircuit(5, 5)

    # Step 1: Create superpositions
    for q in range(5):
        qc.h(q)

    # Step 2: Entangle pairs
    qc.cx(0, 1)
    qc.cx(2, 3)
    qc.cx(1, 4)

    # Step 3: Controlled phase kickback
    qc.cp(0.7, 3, 4)
    qc.cp(1.2, 0, 2)

    # Step 4: Interference layer
    for q in range(5):
        qc.ry(0.4 * q, q)
        qc.rz(0.2 * (5 - q), q)

    # Step 5: Invert and echo
    qc.swap(0, 4)
    qc.ch(2, 1)
    qc.cz(3, 0)

    # Step 6: Barrier and measurement
    qc.barrier()
    qc.measure(range(5), range(5))
    with open("advanced_circuit.qasm", "w") as f:
        qiskit.qasm3.dump(qc, f)

def computeDelay(numElements, duration):
    t = np.linspace(0, 1, numElements)
    y0 = np.tanh(np.log(t+1))
    total = sum(y0)
    y_new = y0*duration/total
    return y_new

def readCircuit():
    qc = load_qasm("advanced_circuit.qasm")

    # Measure all if needed
    if not any(inst[0].name == 'measure' for inst in qc.data):
        qc.measure_all()

    # Rename classical register to 'c0'
    qc = standardize_classical_register(qc, new_name="c0")

    # Save image
    circuit_drawer(qc, output='mpl', filename='quantum_circuit_1.png')

    return qc

def standardize_classical_register(qc: QuantumCircuit, new_name="c0") -> QuantumCircuit:
    num_qubits = qc.num_qubits
    num_clbits = qc.num_clbits

    # Create new registers
    new_qreg = QuantumRegister(num_qubits, name="q0")
    new_creg = ClassicalRegister(num_clbits, name=new_name)

    # Build a new circuit with renamed registers
    new_qc = QuantumCircuit(new_qreg, new_creg)

    # Map old clbits/qbits to new ones
    qmap = {old: new for old, new in zip(qc.qubits, new_qreg)}
    cmap = {old: new for old, new in zip(qc.clbits, new_creg)}

    # Copy instructions
    for instr, qargs, cargs in qc.data:
        qargs_mapped = [qmap.get(q, q) for q in qargs]
        cargs_mapped = [cmap.get(c, c) for c in cargs]
        new_qc.append(instr, qargs_mapped, cargs_mapped)

    return new_qc

def rank_scores():
    qc = readCircuit()

    # Run the circuit: 1 = use simulator, 0 = use real backend
    # result = ibm_qc_interface.quantum_execute(simulator=1, circuit=qc)
    result = noisy_simulator(qc) 
    best = max(result, key = result.get)
    score_sorted = sorted(result.items(), key=lambda x: x[1], reverse=False)
    # return f"The best score is {best} and the rest of the results for comparison are {score_sorted}"
    return score_sorted