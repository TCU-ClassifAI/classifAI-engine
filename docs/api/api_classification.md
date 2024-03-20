# API Reference

!!! abstract "API KEY INSTRUCTIONS"

    Ensure that you include your API key in all requests by using the following format: curl -H "X-API-KEY: MYAPIKEY" https://api.mydomain.com/v1/users. [Need an API key or instructions on how to obtain one?](mailto:meow)

### Categorization 

#### categorize_transcript

* **URL:**
  `/categorize/categorize_transcript`

* **Method:**
  `POST`

* **Data Params:**
  JSON array of objects with the following fields:
  - `end_time` (int)
  - `speaker` (string)
  - `start_time` (int)
  - `text` (string)

* **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    [
      {
        "end_time": 2301,
        "level": 1,
        "question": "Why did you bring me here? ",
        "speaker": "Speaker 0",
        "start_time": 1260,
      }
    ]
    ```


## EXAMPLES:

CURL: 
```json
curl -X POST -H "Content-Type: application/json"      -d '[
    {
      "end_time": 2301,
      "speaker": "Speaker 0",
      "start_time": 1260,
      "text": "Why did you bring me here? "
    },
    {
      "end_time": 4263,
      "speaker": "Main Speaker",
      "start_time": 3242,
      "text": "I dont like going out. "
    }
  ]' localhost:5000/categorize/categorize_transcript
```
RESPONSE:

```json
[
  {
    "end_time": 2301,
    "level": 1,
    "question": "Why did you bring me here? ",
    "speaker": "Speaker 0",
    "start_time": 1260,
  }
]
```