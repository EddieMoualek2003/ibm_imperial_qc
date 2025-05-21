## Module Imports.
import argparse
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile

## IBM Quantum Computer Interface Module Import
import ibm_qc_interface

def map_board(lights, qc, qr):
    j = 0
    for i in lights:
        if i == 1:
            qc.x(qr[j])
            j += 1
        else:
            j += 1

# Initialize
def initialize_smart(l, qc, tile, flip, oracle):
    map_board(l, qc, tile)
    qc.h(flip[:3])
    qc.x(oracle[0])
    qc.h(oracle[0])

def flip_1(qc, flip, tile):
    # push 0
    qc.cx(flip[0], tile[0])
    qc.cx(flip[0], tile[1])
    qc.cx(flip[0], tile[3])
    # push 1
    qc.cx(flip[1], tile[0])
    qc.cx(flip[1], tile[1])
    qc.cx(flip[1], tile[2])
    qc.cx(flip[1], tile[4])
    # push 2
    qc.cx(flip[2], tile[1])
    qc.cx(flip[2], tile[2])
    qc.cx(flip[2], tile[5])

def inv_1(qc, flip, tile):
    # copy 0,1,2
    qc.cx(tile[0], flip[3])
    qc.cx(tile[1], flip[4])
    qc.cx(tile[2], flip[5])

def flip_2(qc, flip, tile):
    # apply flip[3,4,5]
    qc.cx(flip[3], tile[0])
    qc.cx(flip[3], tile[3])
    qc.cx(flip[3], tile[4])
    qc.cx(flip[3], tile[6])
    qc.cx(flip[4], tile[1])
    qc.cx(flip[4], tile[3])
    qc.cx(flip[4], tile[4])
    qc.cx(flip[4], tile[5])
    qc.cx(flip[4], tile[7])
    qc.cx(flip[5], tile[2])
    qc.cx(flip[5], tile[4])
    qc.cx(flip[5], tile[5])
    qc.cx(flip[5], tile[8])

def inv_2(qc, flip, tile):
    # copy 3,4,5
    qc.cx(tile[3], flip[6])
    qc.cx(tile[4], flip[7])
    qc.cx(tile[5], flip[8])

def flip_3(qc, flip, tile):
    qc.cx(flip[6], tile[3])
    qc.cx(flip[6], tile[6])
    qc.cx(flip[6], tile[7])
    qc.cx(flip[7], tile[4])
    qc.cx(flip[7], tile[6])
    qc.cx(flip[7], tile[7])
    qc.cx(flip[7], tile[8])
    qc.cx(flip[8], tile[5])
    qc.cx(flip[8], tile[7])
    qc.cx(flip[8], tile[8])

def lights_out_oracle(qc, tile, oracle, auxiliary):
    qc.x(tile[6:9])
    qc.mcx(tile[6:9], oracle[0], auxiliary, mode="basic")
    qc.x(tile[6:9])

def diffusion(qc, flip):
    qc.h(flip[:3])
    qc.x(flip[:3])
    qc.h(flip[2])
    qc.ccx(flip[0], flip[1], flip[2])
    qc.h(flip[2])
    qc.x(flip[:3])
    qc.h(flip[:3])

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--console",
        help="Displays the lights out grid in the console",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--delay",
        help="Sets the delay (in seconds) between iteration steps for the LED array and console",
        required=False,
        type=float,
        default=1.0,
    )
    parser.add_argument(
        "-b",
        "--brightness",
        help="Sets the brightness of LEDs, between 0.0 and 1.0",
        required=False,
        type=float,
        default=1.0,
    )
    return parser.parse_args()

def compute_quantum_solution(lights):
    # Initialize quantum circuit board
    tile = QuantumRegister(9)
    flip = QuantumRegister(9)
    oracle = QuantumRegister(1)
    auxiliary = QuantumRegister(1)
    result = ClassicalRegister(9, name="c0")
    # 20 qubit
    qc = QuantumCircuit(tile, flip, oracle, auxiliary, result)

    initialize_smart(l = lights, qc = qc, tile=tile, flip=flip, oracle=oracle)
    for i in range(2):
        flip_1(qc=qc, flip=flip, tile=tile)
        inv_1(qc=qc, flip=flip, tile=tile)
        flip_2(qc=qc, flip=flip, tile=tile)
        inv_2(qc=qc, flip=flip, tile=tile)
        flip_3(qc=qc, flip=flip, tile=tile)

        lights_out_oracle(qc, tile, oracle, auxiliary)

        flip_3(qc=qc, flip=flip, tile=tile)
        inv_2(qc=qc, flip=flip, tile=tile)
        flip_2(qc=qc, flip=flip, tile=tile)
        inv_1(qc=qc, flip=flip, tile=tile)
        flip_1(qc=qc, flip=flip, tile=tile)

        diffusion(qc, flip)
    # Uncompute
    qc.h(oracle[0])
    qc.x(oracle[0])

    # get the whole solution from the top row of the solution
    # If you get a solution, you don't need to erase the board, so you don't need the flip_3 function.
    flip_1(qc, flip, tile)
    inv_1(qc, flip, tile)
    flip_2(qc, flip, tile)
    inv_2(qc, flip, tile)

    # Measuremnt
    qc.measure(flip, result)

    # Make the Out put order the same as the input.
    qc = qc.reverse_bits()
    result = ibm_qc_interface.quantum_execute(simulator=1, circuit=qc)
    results_dict = result[0].data.c0.get_counts()
    score_sorted = sorted(results_dict.items(), key=lambda x: x[1], reverse=True)
    final_score = score_sorted[0:40]
    quantum_solution = final_score[0][0]
    return quantum_solution