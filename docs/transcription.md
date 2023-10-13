# Transcription

Transcription is done by the transcirption service. 

We use a GPU server with whisper

## Transcription format

We store the transcription to a database. The transcription is stored in a json format. 

```json
{
    "transcription": [
        {
            "word": "hello",
            "start": 0.0,
            "end": 0.5
        },
        {
            "word": "world",
            "start": 0.5,
            "end": 1.0
        }
    ]
}
```