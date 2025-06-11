from shor_demo_v2.shor_update_v2 import *
from shor_demo_v2.shor_functions import *
from random import randint
from sympy import isprime
from math import gcd, log2, ceil

def shor_func(N, a):
    m_target = ceil(log2(N))
    n_count = 2 * m_target
    qc = create_shor_qpe_circuit(n_count, m_target, a, N)
    counts = measure(qc)
    frequency = result_clean_convert(counts)
    factor = find_factors(frequency, n_count, N, a)
    return factor, frequency

def shor_game():
    print("🎮 Welcome to the Shor's Algorithm Game!")
    numTries = 0
    maxTries = 5
    found = False

    # Select composite N
    while True:
        N = 55
        if not isprime(N):
            break

    print(f"\n🔢 The number to be factored is: {N}")
    m_target = ceil(log2(N))
    n_count = 2 * m_target
    a_used = []

    while not found and numTries < maxTries:
        print(f"\n🔁 Attempt {numTries + 1} of {maxTries}")

        # Alternate: even = human, odd = quantum

        try:
            guess = 1#int(input("🧑‍💻 Your turn! Enter a guess for a nontrivial factor of N: "))
            if guess in [1, N]:
                print("❌ Trivial factor. Try something else.")
            elif N % guess == 0:
                print(f"✅ Well done! {guess} is a factor of {N}. You win!")
                found = True
            else:
                print(f"❌ {guess} is not a factor. Let's see what quantum can do...")
        except ValueError:
            print("⚠️ Invalid input. Skipping your turn.")

        if not found:
            # Quantum Turn
            a = randint(2, N - 1)
            if a in a_used:
                continue
            a_used.append(a)

            if gcd(a, N) != 1:
                print(f"⚛️ Quantum Turn: Found factor immediately via gcd: {gcd(a, N)}")
                found = True
                break

            print(f"⚛️ Quantum Turn: Running with a = {a}")
            factor, frequency = shor_func(N, a)

            # factor = find_factors(frequency, n_count, N, a)
            if factor != 0:
                print(f"✅ Quantum computer found a factor: {factor}.")
                found = True
            else:
                print("❌ Quantum attempt failed.")
        
        numTries += 1

    if not found:
        print("\n🚫 Game over. Neither you nor the quantum computer found a factor.")
