#####################
# THIS IS THE MODIFIED VERSION FOR THE NEW PLATFORM
#####################

## Standard Python Module Imports
import numpy as np
import math
import time
from random import choice

## Modulation of "lights_out" Functions for Improved Readability.
import lights_out_consants
from lights_out_func import *
from lights_out_display import *

## Array containing the initial lights out grid values
lights = lights_out_consants.return_lights()

## Dictionary that corelates the grid index to an index on the LED array (Centered in the LED array)
LED_array_indices = lights_out_consants.return_LED_array_indices()

from sense_emu import SenseHat

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
    results_dict = result
    score_sorted = sorted(results_dict.items(), key=lambda x: x[1], reverse=True)
    final_score = score_sorted[0:40]
    quantum_solution = final_score[0][0]
    return quantum_solution

import time

def visualize_solution_on_sensehat(hat, initial_grid, bitstring_solution, delay=1.0):
    """
    Visualizes the Lights Out solution on the Sense HAT LED matrix.
    Displays initial grid, animates presses, and shows final state.

    Args:
        initial_grid (list of int): List of 9 binary values representing lights ON/OFF.
        bitstring_solution (str): 9-bit string from quantum circuit (e.g., '101000010').
        delay (float): Time to wait between animation steps in seconds.
    """

    # Setup
    sense = hat
    sense.clear()

    # Color definitions
    ON_COLOR = (0, 0, 255)       # Blue
    OFF_COLOR = (20, 20, 20)     # Grey
    PRESS_COLOR = (255, 0, 0)    # Red

    # Grid layout mapping to center 3x3 on Sense HAT
    index_map = [
        (2, 2), (2, 3), (2, 4),
        (3, 2), (3, 3), (3, 4),
        (4, 2), (4, 3), (4, 4)
    ]

    # Copy grid
    grid = initial_grid.copy()

    # Helper to display current state
    def display_grid(active_index=None):
        for i, val in enumerate(grid):
            x, y = index_map[i]
            if i == active_index:
                color = PRESS_COLOR
            else:
                color = ON_COLOR if val == 1 else OFF_COLOR
            sense.set_pixel(x, y, color)

    # Helper to toggle value
    def switch(val): return 0 if val == 1 else 1

    # Initial display
    display_grid()
    time.sleep(delay)

    # Execute each press step
    for i, bit in enumerate(bitstring_solution):
        if bit == '1':
            # Highlight the press
            display_grid(active_index=i)
            time.sleep(delay)

            # Toggle self and neighbors
            grid[i] = switch(grid[i])
            neighbors = []

            if i - 3 >= 0: neighbors.append(i - 3)   # above
            if i + 3 < 9:  neighbors.append(i + 3)   # below
            if i % 3 != 0: neighbors.append(i - 1)   # left
            if i % 3 != 2: neighbors.append(i + 1)   # right

            for j in neighbors:
                grid[j] = switch(grid[j])

            # Display updated grid
            display_grid()
            time.sleep(delay)

    # Final state
    display_grid()

def return_lights():
    return [
    [0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 0, 1],
    [0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def return_LED_array_indices():
    return {
    0: [38, 41, 37, 42],
    1: [46, 49, 45, 50],
    2: [54, 53, 57, 58],
    3: [36, 43, 155, 148],
    4: [44, 51, 147, 140],
    5: [52, 59, 139, 132],
    6: [154, 149, 153, 150],
    7: [146, 141, 145, 142],
    8: [138, 133, 137, 134],
}

## Main function the can be called and ran.
def lights_out_main(**kwargs):
    args = parse_arguments()
    hat = SenseHat()
    try:
        while True:
            print("Starting Quantum Lights Out Solver!")
            print("Choosing random grid arrangement...")
            lights_grid = choice(lights).copy()
            print("Grid chosen:", lights_grid)
            print("Computing quantum solution...")
            quantum_solution = compute_quantum_solution(lights_grid)
            print(f"Quantum solution found! {quantum_solution}")
            print("Visualizing solution...")
            visualize_solution_on_sensehat(hat = hat, initial_grid=lights_grid, bitstring_solution=quantum_solution)
            # visualize_solution(lights_grid, quantum_solution, args)
            print("\n")
    except Exception as e:
        print("An error occured: ", e)

## Main call
if __name__ == "__main__":
    lights_out_main()