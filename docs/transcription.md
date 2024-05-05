# Jobs: Transcription

Transcription is done by the transcription worker. The worker uses the whisper library to transcribe audio files, and NeMo to diarize and align the transcription to the audio.


## Transcription format

Recall that you can check the status of a job by sending a GET request to `get_transcription_status` with the `job_id` as a query parameter, like so:

```sh
curl http://localhost:5000/transcription/get_transcription_status?job_id=3c73dd07-66ff-48ab-9f4e-e6726987c06f
```


A job status will look like this:

```json
{
  "meta": {
    "job_id": "3c73dd07-66ff-48ab-9f4e-e6726987c06f",
    "job_type": "transcription",
    "message": "Aligning audio",
    "status": "aligning"
  },
  "status": "started"
}
```

When the job is completed, the status will look like this:

```json
{
  "meta": {
    "job_id": "3c73dd07-66ff-48ab-9f4e-e6726987c06f",
    "job_type": "transcription",
    "message": "Transcription and diarization completed",
    "status": "completed"
  },
  "result": "{\"job_id\": \"3c73dd07-66ff-48ab-9f4e-e6726987c06f\", \"type\": \"transcription\", \"status\": \"completed\", \"submit_time\": 1710546893.69, \"duration\": 0, \"result\": \"[{'speaker': 'Speaker 1', 'start_time': 7900, 'end_time': 11700, 'text': \\\"Our next guest is a true American hero, and he's only eight years old. \\\"}, {'speaker': 'Speaker 2', 'start_time': 12181, 'end_time': 19684, 'text': \\\"Last week, Lucas Armitage bravely defended his family and his home when he stopped an intruder all by himself just by using his daddy's gun. \\\"}, {'speaker': 'Speaker 1', 'start_time': 19704, 'end_time': 23125, 'text': \\\"That's right, and Lucas and his dad, Jack, are with us in the studio this morning. \\\"}, {'speaker': 'Speaker 1', 'start_time': 23165, 'end_time': 24226, 'text': 'Good morning to both of you. '}, {'speaker': 'Speaker 1', 'start_time': 24246, 'end_time': 25286, 'text': 'Hi, guys. '}, {'speaker': 'Speaker 1', 'start_time': 25326, 'end_time': 27047, 'text': 'Now, Lucas, can you tell us what happened? '}, {'speaker': 'Speaker 0', 'start_time': 27592, 'end_time': 31094, 'text': 'I heard the noise, and I got up from bed and went into the kitchen door. '}, {'speaker': 'Speaker 2', 'start_time': 31114, 'end_time': 31915, 'text': 'Dad keeps the gun. '}, {'speaker': 'Speaker 1', 'start_time': 32115, 'end_time': 34216, 'text': 'So you found it all by yourself, right? '}, {'speaker': 'Speaker 0', 'start_time': 34416, 'end_time': 35377, 'text': 'I take it out a lot. '}, {'speaker': 'Speaker 0', 'start_time': 35577, 'end_time': 36658, 'text': 'Sometimes I just look at it. '}, {'speaker': 'Speaker 1', 'start_time': 36758, 'end_time': 36938, 'text': 'Right. '}, {'speaker': 'Speaker 1', 'start_time': 36978, 'end_time': 39640, 'text': \\\"Now, it was a burglar, wasn't it, Lucas? \\\"}, {'speaker': 'Speaker 1', 'start_time': 39660, 'end_time': 41041, 'text': 'He was trying to steal things. '}, {'speaker': 'Speaker 0', 'start_time': 41201, 'end_time': 41901, 'text': 'He looked hungry. '}, {'speaker': 'Speaker 0', 'start_time': 42121, 'end_time': 45784, 'text': \\\"When he saw I had the gun, he put his hands up and said, please don't shoot. \\\"}, {'speaker': 'Speaker 1', 'start_time': 45924, 'end_time': 47885, 'text': \\\"But you didn't listen to him, did you? \\\"}, {'speaker': 'Speaker 0', 'start_time': 47905, 'end_time': 49606, 'text': 'I know it would be easy to shoot him. '}, {'speaker': 'Speaker 0', 'start_time': 49646, 'end_time': 50907, 'text': 'Just aim and pull the trigger. '}, {'speaker': 'Speaker 2', 'start_time': 51407, 'end_time': 51767, 'text': \\\"That's right. \\\"}, {'speaker': 'Speaker 2', 'start_time': 51787, 'end_time': 53768, 'text': \\\"Well, and that's exactly what you did, right? \\\"}, {'speaker': 'Speaker 1', 'start_time': 53808, 'end_time': 54928, 'text': \\\"You shot him in the leg, didn't you? \\\"}, {'speaker': 'Speaker 1', 'start_time': 54948, 'end_time': 56688, 'text': 'You put one right through the kneecap, right? '}, {'speaker': 'Speaker 0', 'start_time': 56708, 'end_time': 61410, 'text': 'Yeah, it was like bang, really loud, and he fell down screaming, and there was lots of blood coming out. '}, {'speaker': 'Speaker 0', 'start_time': 61430, 'end_time': 62470, 'text': 'Lucas, you really are a hero. '}, {'speaker': 'Speaker 0', 'start_time': 62510, 'end_time': 65150, 'text': 'He started crawling away and crying, so I shot him in the back. '}, {'speaker': 'Speaker 1', 'start_time': 65191, 'end_time': 67471, 'text': 'Yeah, you must be so proud of your son, Jack. '}, {'speaker': 'Speaker 0', 'start_time': 67491, 'end_time': 70112, 'text': 'And then I stood over him and shot him like bang, bang. '}, {'speaker': 'Speaker 1', 'start_time': 70891, 'end_time': 74593, 'text': \\\"Well, that's one crook that's not gonna be breaking into anybody else's home, is he? \\\"}, {'speaker': 'Speaker 0', 'start_time': 74613, 'end_time': 74853, 'text': 'Yeah. '}, {'speaker': 'Speaker 0', 'start_time': 74973, 'end_time': 77134, 'text': \\\"He wouldn't stop talking, so then I shut his jaw. \\\"}, {'speaker': 'Speaker 0', 'start_time': 77254, 'end_time': 78815, 'text': \\\"Well, how'd you manage to do that, Lucas? \\\"}, {'speaker': 'Speaker 0', 'start_time': 78975, 'end_time': 82737, 'text': 'Either you shoot at the temples and pull down, or you shoot at the side of the skull wall. '}, {'speaker': 'Speaker 3', 'start_time': 82817, 'end_time': 84278, 'text': \\\"It's the weakest part of the skull, he's right. \\\"}, {'speaker': 'Speaker 1', 'start_time': 84338, 'end_time': 86299, 'text': \\\"That's very sophisticated knowledge there. \\\"}, {'speaker': 'Speaker 0', 'start_time': 86519, 'end_time': 88300, 'text': 'Yeah, but then he started screaming. '}, {'speaker': 'Speaker 0', 'start_time': 88480, 'end_time': 89021, 'text': 'Yeah, right. '}, {'speaker': 'Speaker 0', 'start_time': 89061, 'end_time': 92043, 'text': 'And then I showed off each one of his fingers, and then he stopped screaming. '}, {'speaker': 'Speaker 2', 'start_time': 92063, 'end_time': 95805, 'text': 'So, Jack, it was the screaming you heard that woke you up so you could call the police? '}, {'speaker': 'Speaker 3', 'start_time': 95825, 'end_time': 96185, 'text': 'No, no. '}, {'speaker': 'Speaker 3', 'start_time': 96265, 'end_time': 98807, 'text': 'Actually, it was Lucas laughing that woke me up. '}, {'speaker': 'Speaker 3', 'start_time': 98907, 'end_time': 100628, 'text': 'I had never heard the kid laugh so hard. '}, {'speaker': 'Speaker 0', 'start_time': 100668, 'end_time': 101889, 'text': 'There was blood all over me. '}, {'speaker': 'Speaker 3', 'start_time': 102089, 'end_time': 103970, 'text': 'Yeah, he smeared it all over himself. '}, {'speaker': 'Speaker 3', 'start_time': 104050, 'end_time': 104471, 'text': 'Really? '}, {'speaker': 'Speaker 0', 'start_time': 104511, 'end_time': 106632, 'text': 'I liked the way the blood made me feel. '}, {'speaker': 'Speaker 1', 'start_time': 106672, 'end_time': 109674, 'text': 'Now, your school gave you a special award for courage, right? '}, {'speaker': 'Speaker 1', 'start_time': 109794, 'end_time': 111915, 'text': 'We have a photograph of that award ceremony. '}, {'speaker': 'Speaker 2', 'start_time': 111935, 'end_time': 112556, 'text': \\\"Let's take a look. \\\"}, {'speaker': 'Speaker 3', 'start_time': 112856, 'end_time': 116197, 'text': \\\"Oh, Lucas, you didn't even change your shirt before you got your award. \\\"}, {'speaker': 'Speaker 3', 'start_time': 116217, 'end_time': 117237, 'text': 'Well, why would he change his shirt? '}, {'speaker': 'Speaker 3', 'start_time': 117257, 'end_time': 118037, 'text': \\\"That's his honor shirt. \\\"}, {'speaker': 'Speaker 0', 'start_time': 118137, 'end_time': 119017, 'text': 'I want the blood. '}, {'speaker': 'Speaker 1', 'start_time': 119117, 'end_time': 122278, 'text': 'Yeah, it must have been fun getting that award at school, right? '}, {'speaker': 'Speaker 0', 'start_time': 122298, 'end_time': 123298, 'text': 'I want the blood. '}, {'speaker': 'Speaker 1', 'start_time': 125038, 'end_time': 127999, 'text': \\\"Well, he's gotten a little shy now. \\\"}, {'speaker': 'Speaker 2', 'start_time': 128318, 'end_time': 130439, 'text': 'Well, Jack Armitage, thanks so much for being here. '}, {'speaker': 'Speaker 2', 'start_time': 130499, 'end_time': 132160, 'text': 'Lucas, thank you for your heroic work. '}, {'speaker': 'Speaker 1', 'start_time': 132320, 'end_time': 133040, 'text': 'Absolutely. '}, {'speaker': 'Speaker 1', 'start_time': 133080, 'end_time': 138221, 'text': 'Now you stick with us because after the break, some warning signs that your pet may be a CIA mole. '}]\", \"job_info\": \"{\\\"audio_path\\\": \\\"output/test.mp3\\\", \\\"model_id\\\": null}\"}",
  "status": "finished"
}
```

## Status Messages and their meanings

### Once a job is started, the status will be `started`. The `meta` object will contain the `job_id`, `job_type`, `message`, and `status`.


The different statuses, and their respective messages within the `meta` object are, in order:

1. queued
   - "Job is queued"
2. downloading
    - "Downloading MP3 file from URL"
    - Note: This status is only applicable if the audio file is being downloaded from a URL.
3. start_transcribing
    - "Transcribing audio"
4. splitting
    - "Splitting audio into vocals and accompaniment for faster processing"
5. loading_nemo
    - "Loading NeMo process for diarization"
6. transcribing
    - "Transcribing audio with Whisper"
7. loading_align_model
    - "Loading align model"
8. aligning
    - "Aligning audio"
9. diarizing
    - "Diarizing audio"
    - Note: Diarization happens in parallel with transcription. This only shows if transcription is completed before diarization.
10. transcription_finished
    - "Transcription completed"
11. extracting_questions
    - "Extracting questions"
12. categorizing_questions
    - "Categorizing questions using LLaMA"
13. summarizing
    - "Summarizing the transcription"
14. combining_results
    - "Combining results"
15. completed
    - "Transcription and diarization completed"

Other possible statuses are:
failed
error

### Once a job is completed, the status will be `finished`. The `meta` object will contain the `job_id`, `job_type`, `message`, and `status`, and the `result` object will contain the `job_id`, `type`, `status`, `submit_time`, `duration`, `result`, and `job_info`.


---

If an error occurs, the status will be `error`, and the `message` will be:

    "An error occured: {error message}"
