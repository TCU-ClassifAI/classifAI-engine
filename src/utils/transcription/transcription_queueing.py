import queue
import threading


transcription_queue = queue.Queue()

def youtube_transcribe_and_diarize(url: str, model_id: str = "large-v3"):
    transcription_queue.put((url, model_id))  # Enqueue the task

def worker_thread():
    while True:
        task = transcription_queue.get()
        url, model_id = task
        result = transcribe_and_diarize(url, model_id)
        # ... (Handle result and potentially signal completion)

threading.Thread(target=worker_thread, daemon=True).start()  # Start worker thread