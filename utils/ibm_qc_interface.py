## Module Imports
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.primitives import StatevectorSampler

# 

def noisy_simulator(qc):
    # Use fake noisy backend
    fake_backend = FakeManilaV2()
    noise_model = NoiseModel.from_backend(fake_backend)
    simulator = AerSimulator(noise_model=noise_model)

    # Transpile circuit
    qc_t = transpile(qc, simulator)
    # Run simulation
    job = simulator.run(qc_t, shots=1024)
    result = job.result()
    counts = result.get_counts()
    return counts

def ideal_simulator(qc):
    """
    Simulate the quantum circuit on the ideal (noise-free) Aer simulator.
    """
    simulator = AerSimulator()
    qc_t = transpile(qc, simulator)
    job = simulator.run(qc_t, shots=1024)
    result = job.result()
    counts = result.get_counts()
    return counts



# def ibm_account_connect():
#     token = "4Ke_JAy6uepzHTBV9fSDjGbFrSse7VYWwRgHJULxx34q"
#     instance = "crn:v1:bluemix:public:quantum-computing:us-east:a/737dfb0b1e374ec7a5772fdbcece5643:a48276b9-a41b-449c-8d76-d2adf66ea9d4::"
#     try:
#         QiskitRuntimeService.save_account(
#         token=token,
#         channel="ibm_cloud", # `channel` distinguishes between different account types.
#         instance=instance, # Copy the instance CRN from the Instance section on the dashboard.
#         name="eddie_ibm_qc", # Optionally name this set of credentials.
#         overwrite=True # Only needed if you already have Cloud credentials.
#         )
#     except:
#         print("Account Exists - Continuing.")
#     return None

# ## This version is definitely used for the existing demos.
# def quantum_execute(simulator, circuit):
#     ibm_account_connect()
#     # I cannot be bothered to change qc throughout, even though it would be faster than typing this.
#     qc = circuit

#     if simulator:
#         # print("Simulator Mode")
#         ## Run on the simulator.
#         sampler = StatevectorSampler()
#         pm = generate_preset_pass_manager(optimization_level=1)

#     elif not simulator: 
#         ## Run on the quantum computer.
#         service = QiskitRuntimeService()
#         backend = service.least_busy(
#             simulator=False,
#             operational=True,
#             min_num_qubits=1)
#         sampler = Sampler(mode=backend)
#         pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

#     ## Transpilation of the current circuit.
#     isa_circuit = pm.run(qc)
#     # isa_circuit.draw("mpl", idle_wires=False)
#     # print("Circuit Transpiled")
#     # print("Job Queued")
#     ## Run the job on the quantum computer
#     job = sampler.run([isa_circuit])
#     pub_result = job.result()
#     # print("Job Complete")

#     return pub_result[0].data.c0.get_counts() # pub_result.data.meas.get_counts()

# def quantum_execute_evolved(simulator, circuit):
#     ibm_account_connect()
#     # I cannot be bothered to change qc throughout, even though it would be faster than typing this.
#     qc = circuit

#     if simulator:
#         # print("Simulator Mode")
#         ## Run on the simulator.
#         sampler = StatevectorSampler()
#         pm = generate_preset_pass_manager(optimization_level=1)

#     elif not simulator: 
#         ## Run on the quantum computer.
#         service = QiskitRuntimeService()
#         backend = service.least_busy(
#             simulator=False,
#             operational=True,
#             min_num_qubits=1)
#         sampler = Sampler(mode=backend)
#         pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

#     ## Transpilation of the current circuit.
#     isa_circuit = pm.run(qc)
#     # isa_circuit.draw("mpl", idle_wires=False)
#     # print("Circuit Transpiled")

#     ## Run the job on the quantum computer
#     job = sampler.run([(isa_circuit)])
#     pub_result = job.result()[0]

#     return pub_result.data.meas.get_counts()
