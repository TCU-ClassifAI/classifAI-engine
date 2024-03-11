import time
from transcribe_and_diarize_threaded import transcribe_and_diarize, check_progress
import threading

# Start the long process

result = None
# 1. Start the process in a separate thread
thread = threading.Thread(
            target=transcribe_and_diarize,
            args=("hi")
        )

thread.start()

# Check progress periodically
while True:
    status = check_progress()
    print(f"Current state: {status['state']}, Message: {status['message']}")

    if status['state'] == "complete":
        break

    time.sleep(5)  # Check every 5 seconds

thread.join()  # Wait for the process to complete
time.sleep(1)  # Wait for the final result to be available
print("Process Complete! Result:", result)
