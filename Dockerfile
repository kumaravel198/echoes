# Use a minimal Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script into the container
COPY python-braille-convert.py .

# Define the command to run the script with command-line arguments.
ENTRYPOINT ["python", "python-braille-convert.py"]