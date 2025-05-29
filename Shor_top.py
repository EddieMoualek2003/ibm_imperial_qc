from Shor_functions import *
from random import randint


def run_quantum_circuit(n_count, m_target):
    qc = create_quantum_circuit(n_count, m_target)
    counts = measure(qc)
    frequency = result_clean_convert(counts)
    return frequency

def check_user_guess(N, user_input):
    if N%user_input == 0:
        return True
    else:
        return False

def main():
    # Stop can be changed on whether a solution is found by either the quantum computer/user OR if no solution has been found in 5 turns each
    numTries = 0
    numTriesLim = 5
    found = False
    N = randint(1, 30) # A random 4 digit number.
    print(f"Number to be factored - {N}")
    m_target = ceil(log2(N))      # qubits for output of modular exponentiation
    n_count = 2 * m_target        # qubits for phase estimation
    frequency = run_quantum_circuit(n_count, m_target)
    a_used = []
    print("Circuit Run Completed")
    while (found == False and numTries < numTriesLim):
        user_input = input(f"Guess a factor for {N}, or P for prime: ")
        if user_input.lower() == "p":
            for i in range(2, int(N**0.5)+1):
                if N%i == 0: # The number has a factor
                    print("The number is not prime")
                    break
            else:
                print("Correct, the number is a prime. Next round")
                found = False
        else:
            if check_user_guess(N, int(user_input)):
                found = True
                print("Correct, Well Done. You Beat the Quantum Computer")
            else:
                print("Incorrect - Quantum Computer's Turn")
                a = randint(1, N-1)
                if a not in a_used:
                    a_used.append(a)
                    factor = find_factors(frequency, n_count, N, a)
                    if factor != 0:
                        endword = "try" if numTries+1 == 1 else "tries"
                        print(f"Factor Found: {factor}. This took {numTries + 1} {endword}. Quantum Computer Wins.")
                        found = True
                    else:
                        print("Quantum Computer Failed - Your Turn Again")
                        numTries+=1
                else:
                    continue
while True:
    main()