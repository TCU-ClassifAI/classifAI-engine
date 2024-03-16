# API Reference - Transcription

!!! abstract "API KEY INSTRUCTIONS"

    Ensure that you include your API key in all requests by using the following format: curl -H "X-API-KEY: MYAPIKEY" https://api.mydomain.com/v1/users. [Need an API key or instructions on how to obtain one?](api_key.md)

    At the moment, the API key is not required. However, it will be required in the future.
    At the moment, you cannot access the HTTP API from outside the TCU network. However, everything is set up to work assuming you self-host the API.

## Starting Transcriptions


### Start a Transcription

This endpoint kicks off a transcription job. It returns a job ID that can be used to check the status of the transcription job.

#### HTTP Method and URL

`POST https://llm.cs.tcu.edu:5000/transcription/transcribe`

#### Parameters



Name | Type | Description | Required?
---- | ---- | ----------- | ---------
file | file | This is the audio file. It can be in mp3, wav, etc. [FFMpeg supports many file types](https://ffmpeg.org/ffmpeg-formats.html) | Required
user_id | string | This is the user ID. It is used to identify the user that made the reqeust | Optional
model_type| string| Model Type. Can be "large", "medium", "medium.en", "tiny.en", [more here](https://github.com/openai/whisper/blob/main/model-card.md) | Optional

<!-- #### Example Request

![localhost:5000/transcription/transcribe](../assets/example_start_transcription.png?raw=true "Example Request") -->

#### Example Response

HTTP 200 OK

```json
{
  "job_id":"73f22806-d904-448f-ae84-650bf6f5aa6a",
  "message":"Job enqueued"
}
```

Element | Type | Description
------- | ---- | -----------
job_id | string | This is the job ID, generated using UUID. It can be used to check the status of the transcription job.
model_type | string | This is the model type. It can be "large", "medium", "medium.en", "tiny.en", [more here](https://github.com/openai/whisper/blob/main/model-card.md)
status | string | This is the status of the transcription job. It can be "in progress", "completed", or "error"
state | string | This is the state of the transcription job. It can be "loading model", "loading audio", "transcribing", "uploading", "completed", or "error"
start_time | float | This is the start time of the transcription job. It is a Unix timestamp.
duration | float | This is the duration of the transcription job. It is a Unix timestamp.



#### Error and Status Codes


Code | Message | Meaning
---- | ------- | -------
400 | No file provided | The request did not include a file
400 | Invalid file type | The file type is not supported
400 | Invalid model type | The model type is not supported
400 | Invalid user ID | The user ID is not valid
500 | Internal Server Error | Something went wrong on our end. Please try again later.

### Start a YouTube Transcription

This endpoint kicks off a transcription job. It returns a job ID that can be used to check the status of the transcription job.

#### HTTP Method and URL

`POST https://llm.cs.tcu.edu:5000/transcription/transcribe_yt`


## Get Transcriptions Status


### Get Transcription Status

This endpoint returns the status of a transcription job. It can be used to check the status of a transcription job, or to get the transcription file.

#### HTTP Method and URL

`GET https://llm.cs.tcu.edu:5000/transcription/get_transcription_status?job_id=[INSERT_JOB_ID]`

#### Parameters

[Table that lists all query and path parameters for the endpoint. If this endpoint has query and path parameters, consider listing them in separate tables---one for path parameters, one for query parameters. If there aren't any parameters for this endpoint, replace the table with "None"]

Name | Type | Description | Required?
---- | ---- | ----------- | ---------
job_id | string | This is the job ID. It can be used to check the status of the transcription job, or to get the transcription file. | Required

#### Example Request

![localhost:5000/get_transcription?job_id=a3a8ed6e-f538-4a06-8fd2-4a3f3ff906ee](../assets/example_get_transcription.png?raw=true "Example Request")

Element | Type | Description | Required?
------- | ---- | ----------- | ---------
job_id | string | This is the job ID. It can be used to check the status of the transcription job, or to get the transcription file. | Required

#### Example Response

```json
{
  "job_id": "a3a8ed6e-f538-4a06-8fd2-4a3f3ff906ee",
  "model_type": "tiny.en", 
  "status": "in progress", 
  "state": "loading model", 
  "start_time": 1698877559.0479097, 
  "duration": 22.8137366771698
}
```

Element | Type | Description
------- | ---- | -----------
job_id | string | This is the job ID, generated using UUID. It can be used to check the status of the transcription job, or to get the transcription file.
model_type | string | This is the model type.
status | string | This is the status of the transcription job. It can be "in progress", "completed", "not found", or "error"
state | string | This is the state of the transcription job. It can be "loading model", "loading audio", "transcribing", "uploading", "completed", or "error"
start_time | float | This is the start time of the transcription job. It is a Unix timestamp.
duration | float | This is the duration of the transcription job. It is a Unix timestamp.
end_time | float | This is the end time of the transcription job (if it is completed). It is a Unix timestamp.
transcription_link | string | This is the link to the transcription file (if it is completed). It can be used to download the transcription file. [Looking for the transcription format?](transcription.md)

#### Error and Status Codes

Code | Message | Meaning
---- | ------- | -------
400 | No job ID provided | The request did not include a job ID
404 | Job not found | The job ID provided does not match any transcription jobs.
500 | Internal Server Error | Something went wrong on our end. Please try again later.
