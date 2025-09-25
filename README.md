# Echoes-Insights

Echoes & Insights is an initiative using Google Gemini to make digital information accessible to everyone. The project creates high-quality content like automatic closed captions for the Deaf and hard of hearing, and braille transcriptions for those with low vision, building a more equitable digital landscape.

***

## Python Braille Converter

A Python script that converts English text to Unified English Braille (UEB) and back again. The script is designed to handle a variety of text features including contractions, capitalization, punctuation, and numbers.

### Features

* **Bidirectional Conversion**: Converts text to Braille and Braille back to text.
* **UEB Grade 2 Support**: Implements a wide range of contractions and rules from Unified English Braille Grade 2.
* **Contraction Handling**: Accurately processes whole-word, shortform, and group sign contractions to produce more efficient Braille output.
* **Punctuation and Numbers**: Correctly translates common punctuation and numerical digits using the Braille numeric indicator.
* **Capitalization Rules**: Applies capital signs for single capitalized letters and a double capital sign for fully capitalized words.
* **Command-line Interface**: Easy to use via command-line arguments for file-based conversion.

### How It Works

The script operates in two main modes: `text_to_braille` and `braille_to_text`.

* **`text_to_braille`**: This function tokenizes the input text into words, numbers, and punctuation. It applies a rule-based system, prioritizing longer contractions first to ensure the most concise Braille representation possible. It handles capitalization by inserting the appropriate indicator (`⠠` for single capital, `⠠⠠` for whole words).

* **`braille_to_text`**: This function works in reverse, iterating through the Braille input and matching patterns against a comprehensive reverse map. It correctly interprets indicators for capitalization and numbers to reconstruct the original English text. The reverse map is carefully ordered to handle multi-cell Braille patterns before single-cell ones, preventing incorrect translations.

---

## Docker Container Usage (Inprogress, does not work correctly.)

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
podman build -t braille-converter .
```
#### 3. Run the Conversion
You can now run the container to convert your files. 

```bash
podman run -d -p 8080:80 --name braille-app braille-converter
```

You can then access the website in your browser at `http://localhost:8080`.

**`--rm`**: Removes the container after it exits.

---

### Project Files
+ **`Dockerfile`**: Defines the container image, including the base image and the instructions for running the script.

+ **`braille_converter.html`**: The Python script that performs the text-to-Braille and Braille-to-text conversion.

+ **`README.md`**: This file, providing instructions and project information.

---

The time it takes to learn Grade 2 braille varies significantly from person to person, as it depends on factors like age, motivation, and the amount of time dedicated to practice.

Here are some general estimates and insights from various sources:

For adults: Learning contracted (Grade 2) braille can take over a year to learn fluently. Some courses, like those offered by CNIB, are designed to be completed within 12 months.

For children: Children can often learn braille in the same amount of time it takes a sighted child to learn to read, assuming consistent practice. One source suggests that learning Grade 1 braille can take 6-8 months, while Grade 2 can take about 18 months.


Practice is key: The key to fluency is consistent, daily practice. Many experienced braille readers emphasize that simply knowing the contractions isn't enough; real-world practice with books, bank statements, and other materials is what truly builds fluency.

Learning Grade 1 first: It's often recommended to learn uncontracted (Grade 1) braille first, as Grade 2 is a more complex system with contractions that serve as a type of shorthand.

In summary, while there is no single "average" number, a motivated adult or child who practices regularly can expect to spend at least a year, and potentially more, to become fluent in Grade 2 braille.

