from pynput import keyboard
import time
import threading

def main_loop(stop_event):
    print("Running loop... press ESC to stop.")
    while not stop_event.is_set():
        print("Still running...")
        time.sleep(1)
    print("Stopped.")

def run_with_hotkey():
    stop_event = threading.Event()

    def on_press(key):
        if key == 'p':
            stop_event.set()
            return False  # stop listener

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    main_loop(stop_event)

run_with_hotkey()
