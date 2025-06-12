haha quantum go brrr
(cause it's so cold)

## Modifications Made
### `utils` Folder
 - This folder is holding shared resources between different games and modules.
 - Currently, it contains two files:
    - `ibm_qc_interface.py` which is responsible for holding and running both the ideal and noisy simulator.
        - Inputs are the quantum circuit that needs to be measured.
        - outputs are both the frequency counts, and the number of shots (used for probability based games and demos)
    - `shor_func.py` which is the engine for computing the factors for an input `N`, based on a base `a`.
        - Inputs are `N` and `a`
        - Outputs are `factor` and `frequency`, and the use of these varies on the type of game.
        - An important note is the dependency of this function on the core functions for Shor's algorithm.
        - This makes the function file somewhat quite long, but allows elegant access to it from the two games that make use of it.

### Movement of Games
 - In preparation for writing the shell script that will be used to control everything, the recommended folder structure was to have a folder of the games, and a folder for the utils. The rest of the games will be added in the next couple of days.