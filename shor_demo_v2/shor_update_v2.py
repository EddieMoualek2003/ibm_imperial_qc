from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
import numpy as np
from fractions import Fraction
from math import gcd
from collections import Counter

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



def qft_dagger(circuit, n):
    """Apply the inverse Quantum Fourier Transform to the first n qubits."""
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            circuit.cp(-np.pi / float(2**(j - m)), m, j)
        circuit.h(j)

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

# print(create_shor_qpe_circuit(8, 4, 2, 15).draw(output='text'))
