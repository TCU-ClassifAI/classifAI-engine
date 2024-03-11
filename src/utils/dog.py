import requests

url = 'http://localhost:5001/transcription/get_transcription_status'

job_id = input("Enter the job ID:")

# Send the request
response = requests.get(url, params={'job_id': job_id})\

# Print the response
print(response.text)
