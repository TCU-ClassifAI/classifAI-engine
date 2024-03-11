import requests

url = 'http://llm.cs.tcu.edu:5001/transcription/start_transcription'

file_path = 'D601 Day 1 Audio Only.mp3'

# Open the file 
with open(file_path, 'rb') as audio:
    files = {'file': audio}

    # Send the request (without manually setting the 'Content-Type' header)
    response = requests.post(url, files=files)

    # Print the response
    print(response.text)
