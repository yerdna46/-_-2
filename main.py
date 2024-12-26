import threading
import keyboard
from rx import create
from rx.core import Observer

# Define the observer that writes events to a file
class FileObserver(Observer):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_next(self, value):
        with open(self.file_path, 'a') as f:
            f.write(f"Event: {value}\n")

    def on_error(self, error):
        with open(self.file_path, 'a') as f:
            f.write(f"Error: {error}\n")

    def on_completed(self):
        with open(self.file_path, 'a') as f:
            f.write("Tracker stopped.\n")

# Function to create an observable for keyboard events
def keyboard_observable(observer, _):
    try:
        def handle_event(event):
            observer.on_next(f"Key: {event.name}, Event: {event.event_type}")

        keyboard.hook(handle_event)
        keyboard.wait('ctrl+alt+q')  # Combination to stop the tracker
        observer.on_completed()
    except Exception as e:
        observer.on_error(e)

# Start the keyboard tracker in a separate thread
def start_tracker():
    observable = create(keyboard_observable)
    observer = FileObserver("keyboard_events.log")
    observable.subscribe(observer)

tracker_thread = threading.Thread(target=start_tracker, daemon=True)
tracker_thread.start()

print("Keyboard tracker running. Press 'Ctrl+Alt+Q' to stop.")
tracker_thread.join()
