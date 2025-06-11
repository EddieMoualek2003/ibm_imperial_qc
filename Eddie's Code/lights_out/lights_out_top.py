#####################
# THIS IS THE MODIFIED VERSION FOR THE NEW PLATFORM
#####################

## Standard Python Module Imports
import numpy as np
import math
import time
from random import choice

## Modulation of "lights_out" Functions for Improved Readability.
from lights_out.lights_out_consants import *
from lights_out.lights_out_func import *
from lights_out.lights_out_display import *

## Array containing the initial lights out grid values
lights = return_lights()

## Dictionary that corelates the grid index to an index on the LED array (Centered in the LED array)
LED_array_indices = return_LED_array_indices()

from sense_emu import SenseHat

## Main function the can be called and ran.
def lights_out_main(**kwargs):
    args = parse_arguments()
    hat = SenseHat()
    try:
        print("Starting Quantum Lights Out Solver!")
        print("Choosing random grid arrangement...")
        lights_grid = choice(lights).copy()
        print("Grid chosen:", lights_grid)
        print("Computing quantum solution...")
        start = time.time()
        quantum_solution = compute_quantum_solution(lights_grid)
        end = time.time()
        print(f"Execution time: {end - start:.4f} seconds")
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