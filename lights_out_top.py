#####################
# THIS IS THE MODIFIED VERSION FOR THE NEW PLATFORM
#####################

## Standard Python Module Imports
import numpy as np
import math
import time
from random import choice

## Modulation of "lights_out" Functions for Improved Readability.
from lights_out import lights_out_consants
from lights_out_func import *

## Array containing the initial lights out grid values
lights = lights_out_consants.return_lights()

## Dictionary that corelates the grid index to an index on the LED array (Centered in the LED array)
LED_array_indices = lights_out_consants.return_LED_array_indices()

## Main function the can be called and ran.
def lights_out_main(**kwargs):
    args = parse_arguments()
    try:
        while True:
            print("Starting Quantum Lights Out Solver!")
            print("Choosing random grid arrangement...")
            lights_grid = choice(lights).copy()
            print("Grid chosen:", lights_grid)
            print("Computing quantum solution...")
            quantum_solution = compute_quantum_solution(lights_grid)
            print(f"Quantum solution found! {quantum_solution}")
            # print("Visualizing solution...")
            # visualize_solution(lights_grid, quantum_solution, args)
            print("\n")
    except Exception as e:
        print("An error occured: ", e)

## Main call
if __name__ == "__main__":
    lights_out_main()