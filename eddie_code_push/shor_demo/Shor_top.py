from shor_demo.Shor_functions import *
from random import randint


def run_quantum_circuit(n_count, m_target):
    qc = create_quantum_circuit(n_count, m_target)
    print("Circuit Created")
    counts = measure(qc)
    print("Circuit Measured")
    frequency = result_clean_convert(counts)
    print("Frequency Recorded")
    return frequency


def shor_main():
    print("Started")
    # Stop can be changed on whether a solution is found by either the quantum computer/user OR if no solution has been found in 5 turns each
    numTries = 0
    numTriesLim = 5
    found = False
    N = randint(1, 10) # A random 4 digit number.
    print(f"Number to be factored - {N}")
    m_target = ceil(log2(N))      # qubits for output of modular exponentiation
    n_count = 2 * m_target        # qubits for phase estimation
    frequency = run_quantum_circuit(n_count, m_target)
    a_used = []
    print("Circuit Run Completed")
    while (found == False and numTries < numTriesLim):
        a = randint(1, N-1)
        if a not in a_used:
            a_used.append(a)
            print(f"Testing with a={a}")
            factor = find_factors(frequency, n_count, N, a)
            if factor != 0:
                endword = "try" if numTries+1 == 1 else "tries"
                print(f"Factor Found: {factor}. This took {numTries + 1} {endword}.")
                found = True
            else:
                print("This try failed - Trying again")
                numTries+=1
        else:
            continue
