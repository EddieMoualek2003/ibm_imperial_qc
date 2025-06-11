from qiskit import transpile, QuantumCircuit
from eddie_code_push.utils.ibm_qc_interface import *
import numpy as np
from math import gcd, ceil, log2
from collections import Counter
from fractions import Fraction

def create_quantum_circuit(n_count, m_target):
    # total qubits: counting + target, measured only on counting
    qc = QuantumCircuit(n_count + m_target, n_count)

    # Apply Hadamard to counting qubits
    qc.h(range(n_count))

    # Initialize target register to |1⟩
    qc.x(n_count + 0)

    # Controlled modular multiplication of a^2^j mod N
    for q in range(n_count):
        # Define the "modular multiplication" gate (placeholder)
        mod_gate = QuantumCircuit(m_target, name=f"U_{2**q}")
        mod_gate.unitary(np.identity(2**m_target), range(m_target))  # Identity for now
        mod_gate_gate = mod_gate.to_gate()
        controlled_mod_gate = mod_gate_gate.control()  # Add 1 control qubit

        # Append to the circuit with correct qubit indices
        qc.append(
            controlled_mod_gate, 
            [q] + list(range(n_count, n_count + m_target))  # Control + target
        )
        # Placeholder: normally you'd implement modular exponentiation here

    # Apply inverse QFT to counting qubits
    def qft_dagger(circuit, n):
        """Inverse QFT for n qubits."""
        for qubit in range(n // 2):
            circuit.swap(qubit, n - qubit - 1)
        for j in range(n):
            for m in range(j):
                circuit.cp(-np.pi / float(2**(j - m)), m, j)
            circuit.h(j)

    qft_dagger(qc, n_count)

    # Measure the counting qubits
    qc.measure_all()
    return qc

def measure(qc):
    # Run simulation
    counts = ideal_simulator(qc)
    return counts[0]

def result_clean_convert(counts):
    # Clean results: only take the counting bits
    cleaned_counts = {}
    for bitstring, count in counts.items():
        bits = bitstring.split(' ')[0]  # Only take the counting qubits
        if bits in cleaned_counts:
            cleaned_counts[bits] += count
        else:
            cleaned_counts[bits] = count

    # Convert to decimal and analyze frequencies
    decimal_results = [int(bits, 2) for bits in cleaned_counts for _ in range(cleaned_counts[bits])]
    frequency = Counter(decimal_results)
    return frequency

# Estimate the phase
def estimate_period(measured_value, n_count, N):
    phi = measured_value / (2**n_count)
    frac = Fraction(phi).limit_denominator(N)
    return frac.denominator

def find_factors(frequency, n_count, N, a):
    r_array = []
    exclude_array = [1, N]
    for value, _ in frequency.most_common(5):
        r = estimate_period(value, n_count, N)
        if r % 2 == 0:
            r_array.append(r)

    # Try factoring with valid r values
    for r in r_array:
        x = pow(a, r // 2, N)
        res_array = [gcd(x - 1, N), gcd(x + 1, N)]
        for res in res_array:
            if res not in exclude_array:
                return res
            break
        else:
            return 0
    else:
        return 0
    