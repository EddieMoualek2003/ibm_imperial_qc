from math import ceil, log2, gcd
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
import numpy as np
from fractions import Fraction
from collections import Counter
from utils.ibm_qc_interface import *

def create_shor_qpe_circuit(n_count, m_target, a, N):
    """
    Build the QPE-based circuit used in Shor's algorithm to estimate order r of a mod N.
    """
    qc = QuantumCircuit(n_count + m_target, n_count)

    # Apply Hadamard to counting register
    qc.h(range(n_count))

    # Initialize target register to |1⟩
    qc.x(n_count)

    # Controlled modular exponentiation gates
    for q in range(n_count):
        power = 2 ** q
        mod_gate = QuantumCircuit(m_target)
        mod_gate.append(modular_mult_gate(a, power, N), range(m_target))
        mod_gate_gate = mod_gate.to_gate()
        controlled_mod_gate = mod_gate_gate.control()
        qc.append(controlled_mod_gate, [q] + [n_count + i for i in range(m_target)])

    # Apply inverse QFT
    qft_dagger(qc, n_count)

    # Measure the counting register
    qc.measure(range(n_count), range(n_count))
    return qc

def qft_dagger(circuit, n):
    """Apply the inverse Quantum Fourier Transform to the first n qubits."""
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            circuit.cp(-np.pi / float(2**(j - m)), m, j)
        circuit.h(j)

def modular_mult_gate(a, power, N):
    """
    Create a unitary gate for modular multiplication:
    |x⟩ → |(a^power * x) mod N⟩, padded to nearest power-of-2.
    """
    dim = 2 ** int(np.ceil(np.log2(N)))
    U = np.zeros((dim, dim))

    # Only fill for values < N; rest remain identity
    for x in range(N):
        y = (pow(a, power, N) * x) % N
        U[y, x] = 1

    # Fill identity for x >= N (optional: only if you might land in these states)
    for x in range(N, dim):
        U[x, x] = 1

    # Confirm unitarity (optional debug check)
    if not np.allclose(U @ U.conj().T, np.identity(dim), atol=1e-8):
        raise ValueError("Matrix is not unitary — check logic.")

    return UnitaryGate(U, label=f"U_{a}^{power} mod {N}")

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

def shor_func(N, a):
    print("Running the function")
    m_target = ceil(log2(N))
    n_count = 2 * m_target
    print("parameters computed")
    qc = create_shor_qpe_circuit(n_count, m_target, a, N)
    print("circuit created")
    counts = measure(qc)
    print("Measuring")
    frequency = result_clean_convert(counts)
    print("Cleaning.")
    factor = find_factors(frequency, n_count, N, a)
    return factor, frequency

from math import gcd

def shor_func_mod(N, a):
    if gcd(a, N) != 1:
        print(f"⚠️ Skipping a = {a}, not coprime with N = {N}")
        factor = "ncp"
        frequency = None
    else:
        m_target = ceil(log2(N))
        n_count = 2 * m_target
        qc = create_shor_qpe_circuit(n_count, m_target, a, N)
        counts = measure(qc)
        frequency = result_clean_convert(counts)
        factor = find_factors(frequency, n_count, N, a)
    return factor, frequency
