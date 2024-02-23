import json

# {"job_id": "b6fa585228a44b3f968e8fc52bee3c90", "model_type": "large-v3", "status": "completed", "progress": "completed", "start_time": "2024-02-19 09:48:03.139", "end_time": "2024-02-19 09:48:54.181", "duration": 51041, "result": [{"speaker": "Speaker 3", "start_time": 60, "end_time": 7458, "text": "We will hear argument this morning in Case Nineteen, Thirteen, Ninety-Two, Dobbs v. Jackson Women's Health Organization. "}]}



def extract_questions(transcript: str) -> list:
    questions = []
    transcript = json.loads(transcript)
    for segment in transcript['result']:
        if '?' in segment['text']:
            questions.append(segment['text'])
    return questions


def extract_questions_in_context(transcript: str) -> list:
    """
    Return questions, their speaker, and the start and end time of the question
    Also include the previous and next segments for context, and the speaker of the previous and next segments

    Args:
        transcript (str): the transcript JSON (format is on documenation)

    Returns:
        list: list of dictionaries, each containing the question, speaker, start and end time, previous segment, next segment, previous speaker, and next speaker

    """

    questions = []
    transcript = json.loads(transcript)
    for i, segment in enumerate(transcript['result']):
        if '?' in segment['text']:
            question = {
                "question": segment['text'],
                "speaker": segment['speaker'],
                "start_time": segment['start_time'],
                "end_time": segment['end_time'],
                "previous_segment": transcript['result'][i-1]['text'] if i > 0 else None,
                "next_segment": transcript['result'][i+1]['text'] if i < len(transcript['result']) - 1 else None,
                "previous_speaker": transcript['result'][i-1]['speaker'] if i > 0 else None,
                "next_speaker": transcript['result'][i+1]['speaker'] if i < len(transcript['result']) - 1 else None
            }
            questions.append(question)
    return questions