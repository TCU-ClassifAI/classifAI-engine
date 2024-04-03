# from flask import Response
# from utils.queue_manager import Job, enqueue
# from flask import make_response


# def analyze_audio(audio_path: str, model_name: str = "large-v3") -> Response:
#     """Analyze an audio file using the specified model.

#     Args:
#         audio_path (str): Path to the audio file.
#         model_name (str): Name of the model to use for analysis (default: "large-v3").

#     Returns:
#         Response object with the analysis results.
#     """
#     job = Job("analyze")
#     job.initialize_transcription_job(audio_path, model_name)
#     job_queue = enqueue(job)
#     return make_response(f"Job {job_queue.id} enqueued for analysis", 200)
