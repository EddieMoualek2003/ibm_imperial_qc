"""
Quantum Entanglement Time Challenge Game with:
- Qiskit (IBM Quantum Computer via ibm_qc_interface)
- Sense HAT display (no GPIO LEDs)
- IBM watsonx Assistant for voice guidance
"""


from qiskit import QuantumCircuit
import time
# from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from utils.ibm_qc_interface import noisy_simulator  
from sense_emu import SenseHat

#Watsonx 
authenticator = IAMAuthenticator('api-key')
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url('serviceurl')
session_id = assistant.create_session(assistant_id='assistant-id').get_result()['session_id']

def watson_say(message):
    response = assistant.message(
        assistant_id='assistant-id',
        session_id=session_id,
        input={'text': message}
    ).get_result()
    print("\n💬 Watsonx:", response['output']['generic'][0]['text'])

def get_user_input():
    response = assistant.message(
        assistant_id='assistant-id',
        session_id=session_id,
        input={"message_type": "text", "text": "Please enter your guess for Qubit B (0 or 1):"}
    ).get_result()
    user_text = response['output']['generic'][0].get('text', '')
    print("Your input:", user_text)
    if '1' in user_text:
        return '1'
    elif '0' in user_text:
        return '0'
    else:
        return None

def display_on_hat(hat, qubit_a, qubit_b):
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    OFF = [0, 0, 0]
    pixels = [OFF[:] for _ in range(64)]

    #Display qubit A in top left 2x2 and qubit B in top right 2x2
    color_a = GREEN if qubit_a == '1' else RED
    color_b = GREEN if qubit_b == '1' else RED
    for i in [0, 1, 8, 9]:
        pixels[i] = color_a
    for i in [6, 7, 14, 15]:
        pixels[i] = color_b

    hat.set_pixels(pixels)

#Game
hat = SenseHat()
hat.clear()
score = 0
rounds = 5

watson_say("Welcome to the Quantum Entanglement Time Challenge!")
time.sleep(2)

for i in range(rounds):
    watson_say(f"Round {i+1}. Preparing entangled qubits...")

    #Create entangled circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    #Running
    counts = noisy_simulator(qc)
    outcome = list(counts.keys())[0] 
    qubit_b, qubit_a = outcome[0], outcome[1]

    display_on_hat(hat, qubit_a, '0')  #Display Qubit A, hide B for now
    watson_say(f"Qubit A is measured as {qubit_a}. Please say or type your prediction for Qubit B (0 or 1).")

    prediction = get_user_input()

    if prediction is None:
        watson_say(f"No valid input detected. Qubit B was {qubit_b}.")
    elif prediction == qubit_b:
        watson_say("Correct! As expected from perfect entanglement, Qubit B matches Qubit A.")
        score += 1
    else:
        watson_say(f"Incorrect. Qubit B was actually {qubit_b}.")

    display_on_hat(hat, qubit_a, qubit_b)
    time.sleep(1.5)
    hat.clear()

watson_say(f"Game over. You scored {score} out of {rounds}. Well done!")

#Cleanup
hat.clear()
assistant.delete_session(assistant_id='your-assistant-id', session_id=session_id)