# Use the official image as a parent image.
FROM python:3.11

# Set the working directory.
WORKDIR /app

# Copy the file from your host to your current location.
COPY src/requirements.txt src/requirements-dev.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY src/ ./

# Run the specified command within the container.
EXPOSE 5000

# Run the specified command within the container.
CMD [ "python", "./run.py" ]

