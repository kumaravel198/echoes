
# Docker Container Usage 

Inprogress, does not work correctly. Braille to text fails spectulary. I have no idea text to braille is working. Can't read output.

_Note: I'm creating an offline, containerized environment for a website that includes a braille transcription feature. I'm focusing exclusively on Braille Grade 1 to ensure a high level of accuracy and reliability. Implementing Braille Grade 2's complex contractions and rules accurately is far too challenging for a straightforward script, and I have low confidence in its output. Therefore, I'm leaving the Grade 2 code disabled in the web UI. For those needing Grade 2 support, several excellent, specialized Git projects and libraries are available that handle it much better._  

This project provides a simple website to convert text files to Braille and vice-versa. The tool is packaged in a lightweight container using Podman, allowing it to run consistently across different environments without requiring a local Python installation.

### Prerequisites

To use this project, you need to have **Podman** or **Docker** installed on your system. Podman is a daemonless container engine for developing, managing, and running OCI Containers.

* [Install Podman](https://podman.io/getting-started/installation)

### Getting Started

Follow these steps to build and run the containerized Braille converter.

#### 1. Clone the Repository

First, clone this project to your local machine using Git:

```bash
git clone [https://github.com/your-username/your-repository.git](https://github.com/your-username/your-repository.git)
cd your-repository
```

_Note: Replace the URL with the actual URL of your Git repository._

####  2. Build the Container Image
Navigate into the project directory and build the container image using the provided **`Dockerfile`**. This command creates a new image tagged as **`braille-converter`**.

```bash
docker build -t braille-converter .
# OR
podman build -t braille-converter .
```
#### 3. Run the Conversion
Run the container, mapping the internal port 5000 (Flask server) to an external port (e.g., 8080) on your host machine.

```bash
docker run -d -p 8080:5000 --name braille-app braille-converter
# OR
podman run -d -p 8080:5000 --name braille-app braille-converter
```

You can then access the website in your browser at `http://localhost:8080`.

**`--rm`**: Removes the container after it exits.

---

### Project Files
+ **`Dockerfile`**: Defines the container image for running the Python Flask application.

+ **`python-braille-convert.py`**: The core Python script containing the Braille conversion logic.

+ **`app.py`**: (Required, but user-created) The Flask application to expose the Python logic as an API.    

+ **`braille_converter.html`**:  The web interface (frontend) that uses JavaScript to call the Python backend API.

