import subprocess

def run_Tie_demo():
    try:
        result = subprocess.run(
            ["python3", "tie_demo_original/QuantumRaspberryTie.py"],
            check=True,           # Raises CalledProcessError if return code != 0
            timeout=10            # Optional safety timeout
        )
        print("Tie Game ended successfully.\n")
    except subprocess.TimeoutExpired:
        print("Error: Tie Demo timed out.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running Tie Demo (non-zero exit): {e}\n")
    except FileNotFoundError:
        print("Error: File not found - tie_demo_original/QuantumRaspberryTie.py\n")
