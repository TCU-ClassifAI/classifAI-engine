# Analyze an audio file 

This endpoint kicks off an analysis job. It returns a job ID that can be used to check the status of the analysis job.

## Start an Analysis

### HTTP Method and URL

`POST https://llm.cs.tcu.edu:5000/analyze/`

### Parameters
EITHER
- file: The audio file to be analyzed. This is a local file that is uploaded to the server.
OR
- url: The URL of the audio file to be analyzed. This is a file that is accessible via a URL.

Name | Type | Description | Required?
---- | ---- | ----------- | ---------
file | file | The audio file to be analyzed. This is a local file that is uploaded to the server. | Required if `url` is not provided
url | string | The URL of the audio file to be analyzed. This is a file that is accessible via a URL. | Required if `file` is not provided
model_name | string | The name of the model to use for analysis. Default is (large-v3) (can edit in config) | Optional

### Example Request

```json
{
  "file": "path/to/audio/file",
  "model_name": "large-v3"
}
```

```sh
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=t4yWEt0OSpg"}' http://llm.cs.tcu.edu:5000/analyze
```

### Example Response

```json
{
  "job_id":"73f22806-d904-448f-ae84-650bf6f5aa6a",
  "message":"Job enqueued"
}
```

## Get Analysis Status

### Get Analysis Status

This endpoint returns the status of an analysis job. It can be used to check the status of an analysis job, or to get the analysis results.

### HTTP Method and URL

`GET https://llm.cs.tcu.edu:5000/analyze?job_id=[INSERT_JOB_ID]`

### Parameters

Name | Type | Description | Required?
---- | ---- | ----------- | ---------
job_id | string | The job ID of the analysis job. | Required

### Example Request

```sh
curl -X GET http://llm.cs.tcu.edu:5000/analyze?job_id=73f22806-d904-448f-ae84-650bf6f5aa6a
```

### Example Response

```json
{
  "meta": {
    "job_id": "e8017039-8a41-480e-b80f-3cb5233611a9",
    "job_type": "analyze",
    "message": "Downloading YouTube and converting to mp3",
    "progress": "downloading",
    "title": "Asking Questions in English | Question Structure | Fix Your Grammar Mistakes!"
  },
  "status": "started"
}
```
(Note: The title field will only update once the video has been downloaded, if it is a YouTube video. Otherwise, it will be the audio file name.)

## Final Analysis Results

A full response can be found at this [pastebin link](https://pastebin.com/2HYGYGPX).

Here is a snippet of the response:

```json
{
  "meta": {
        "job_id": "73f22806-d904-448f-ae84-650bf6f5aa6a",
        "job_type": "analyze",
        "message": "Analysis completed",
        "progress": "completed",
        "title": "The title of the video",
    },
    "result": {
        "questions": [
            {
                "question": "What is the title of the video?",
                "level": 1,
                "speaker": "Main Speaker",
                "start_time": 25034,
                "end_time": 26324,
            },
            {
                "question": "What is the video about?",
                "level": 1,
                "speaker": "Main Speaker",
                "start_time": 26324,
                "end_time": 27534,
            }
        ],
        "summary": "One or two sentences summarizing the video",
        "transcript": [
            {
                "speaker": "Main Speaker",
                "start_time": 0,
                "end_time": 1000,
                "text": "The first sentence of the transcript."
            },
            {
                "speaker": "Main Speaker",
                "start_time": 1000,
                "end_time": 2000,
                "text": "The second sentence of the transcript."
            }
        ]
    },
    "status": "finished",
}
```