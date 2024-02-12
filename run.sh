#!/bin/bash

# Generate a unique tag for the Docker image based on current timestamp
TAG="my_image_$(date +"%Y%m%d_%H%M%S")"

# Build the Docker image with the generated tag
docker build --tag "$TAG" .

# Run the Docker container with the generated tag
docker run -d -p 5000:5000 --name my_container "$TAG"

# Display information about the running container
docker ps --filter "name=my_container"
