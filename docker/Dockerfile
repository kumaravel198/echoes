# Dockerfile

# Stage 1: Build the Python application
FROM python:3.9-slim AS build

# Set the working directory
WORKDIR /app

# Copy the Python script and create the Flask application file
COPY python-braille-convert.py .
# The app.py file would need to be created with the content from step 1
# For simplicity, we assume app.py is created in the same directory and contains the conversion functions
# If the conversion functions were properly imported from python-braille-convert.py, you'd only need:
COPY app.py . 

# Install dependencies (Flask, CORS)
RUN pip install flask flask-cors

# Stage 2: Serve the front end and run the backend
# Use a common Python base for the final image
FROM python:3.9-slim

WORKDIR /app

# Copy dependencies and the application code from the build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /app .

# Copy the HTML file into a dedicated directory
COPY braille_converter.html /app/static/index.html

# Expose the port for the Flask app
EXPOSE 5000

# The NGINX approach in the original was for static files.
# For a full Python app, we run the Python server.
# Run the application (using Gunicorn for production-like environment is better)
# For this example, we use the simple Python execution.
CMD ["python", "app.py"]