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

## Docker Container Usage (Inprogress)

_Note: Once the script is more stable, I plan to create a container that allows running a website locally for offline use._  

This project provides a simple command-line tool to convert text files to Braille and vice-versa. The tool is packaged in a lightweight container using Podman, allowing it to run consistently across different environments without requiring a local Python installation.

### Prerequisites

To use this project, you need to have **Podman** installed on your system. Podman is a daemonless container engine for developing, managing, and running OCI Containers.

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
You can now run the container to convert your files. The container needs access to your local files, so you must use a volume mount to share your current directory.

Use the following command, replacing **`[file-name]`** and **`[direction]`** with your desired values.

```bash
podman run --rm --volume "$PWD":/app:z braille-converter [file-name] [to_braille|to_text]
```
**`--rm`**: Removes the container after it exits.

**`--volume "$PWD":/app:z:`** This is a crucial step. It mounts your current local directory (**`$PWD`**) to the **`/app`** directory inside the container, allowing the script to find your files. The **`:z`** option is for systems with SELinux (like Fedora) to ensure correct permissions.

#### Example Usage
To convert sample-text.txt to Braille:

```bash
podman run --rm --volume "$PWD":/app:z braille-converter sample-text.txt to_braille
```
The output will be printed directly to your terminal.

---

### Project Files
+ **`Dockerfile`**: Defines the container image, including the base image and the instructions for running the script.

+ **`python-braille-convert.py`**: The Python script that performs the text-to-Braille and Braille-to-text conversion.

+ **`README.md`**: This file, providing instructions and project information.

---

### Example output from podman for reference

podman run --rm --volume "$PWD":/app:z braille-converter sample-text.txt to_braill

--- Original Content from 'sample-text.txt' ---
Ontario's Human Rights Code, the first in Canada, was enacted in 1962. 

The Code prohibits actions that discriminate against people based on a protected ground  in a protected social area.

Protected grounds are:
Age
Ancestry, colour, race
Citizenship
Ethnic origin
Place of origin
Creed
Disability
Family status
Marital status (including single status)
Gender identity, gender expression
Receipt of public assistance (in housing only)
Record of offences (in employment only)
Sex (including pregnancy and breastfeeding)
Sexual orientation.

Protected social areas are:
Accommodation (housing)
Contracts
Employment
Goods, services and facilities
Membership in unions, trade or professional associations.

For more information:
Guide to your rights and responsibilities under the Human Rights Code
Guidelines on developing human rights policies and procedures
Human Rights Code cards

------------------------------
--- Converted to Braille ---
⠠⠕⠝⠞⠁⠗⠊⠕⠄⠎ ⠠⠓⠥⠍⠁⠝ ⠠⠗⠎ ⠠⠉⠕⠙⠑⠂ ⠮ ⠋⠗ ⠔ ⠠⠉⠁⠝⠁⠙⠁⠂ ⠐⠧ ⠑⠝⠁⠉⠞⠑⠙ ⠔ ⠼⠁⠊⠋⠃⠲ 

⠠⠮ ⠠⠉⠕⠙⠑ ⠏⠗⠕⠓⠊⠃⠭⠎ ⠁⠉⠞⠊⠕⠝⠎ ⠞ ⠙⠊⠎⠉⠗⠊⠍⠔⠁⠞⠑ ⠁⠛⠎⠞ ⠏ ⠃⠁⠎⠑⠙ ⠕⠝ ⠁ ⠏⠗⠕⠞⠑⠉⠞⠑⠙ ⠛⠗⠳⠝⠙  ⠔ ⠁ ⠏⠗⠕⠞⠑⠉⠞⠑⠙ ⠎⠕⠉⠊⠁⠇ ⠁⠗⠑⠁⠲

⠠⠏⠗⠕⠞⠑⠉⠞⠑⠙ ⠛⠗⠳⠝⠙⠎ ⠜⠒
⠠⠁⠛⠑
⠠⠁⠝⠉⠑⠎⠞⠗⠽⠂ ⠉⠕⠇⠳⠗⠂ ⠗⠁⠉⠑
⠠⠉⠭⠊⠵⠑⠝⠩⠊⠏
⠠⠑⠹⠝⠊⠉ ⠕⠗⠊⠛⠔
⠠⠏⠇⠁⠉⠑ ⠷ ⠕⠗⠊⠛⠔
⠠⠉⠗⠑⠑⠙
⠠⠙⠊⠎⠁⠃⠊⠇⠔⠞⠽
⠠⠋⠁⠍⠊⠇⠽ ⠎⠞⠁⠞⠥
⠠⠍⠁⠗⠭⠁⠇ ⠎⠞⠁⠞⠥ ⠣⠔⠉⠇⠥⠙⠔ ⠎⠔⠇⠑ ⠎⠞⠁⠞⠥⠜
⠠⠛⠑⠝⠙⠑⠗ ⠊⠙⠑⠝⠞⠔⠞⠽⠂ ⠛⠑⠝⠙⠑⠗ ⠑⠭⠏⠗⠑⠎⠎⠊⠕⠝
⠠⠗⠑⠉⠑⠊⠏⠞ ⠷ ⠏⠥⠃⠇⠊⠉ ⠁⠎⠎⠊⠎⠞⠁⠝⠉⠑ ⠣⠔ ⠓⠕⠥⠎⠔ ⠕⠝⠇⠽⠜
⠠⠗⠑⠉⠕⠗⠙ ⠷ ⠕⠋⠋⠢⠉⠑⠎ ⠣⠔ ⠑⠍⠏⠇⠕⠽⠍⠑⠝⠞ ⠕⠝⠇⠽⠜
⠠⠎⠑⠭ ⠣⠔⠉⠇⠥⠙⠔ ⠏⠗⠑⠛⠝⠁⠝⠉⠽ ⠯ ⠃⠗⠑⠁⠎⠞⠋⠑⠑⠙⠔⠜
⠠⠎⠑⠭⠥⠁⠇ ⠕⠗⠊⠑⠝⠞⠁⠞⠊⠕⠝⠲

⠠⠏⠗⠕⠞⠑⠉⠞⠑⠙ ⠎⠕⠉⠊⠁⠇ ⠁⠗⠑⠁⠎ ⠜⠒
⠠⠁⠉⠉⠕⠍⠍⠕⠙⠁⠞⠊⠕⠝ ⠣⠓⠕⠥⠎⠔⠜
⠠⠉⠕⠝⠞⠗⠁⠉⠞⠎
⠠⠑⠍⠏⠇⠕⠽⠍⠑⠝⠞
⠠⠛⠙⠎⠂ ⠎⠑⠗⠧⠊⠉⠑⠎ ⠯ ⠋⠁⠉⠊⠇⠭⠊⠑⠎
⠠⠍⠑⠍⠐⠃⠗⠩⠊⠏ ⠔ ⠥⠝⠊⠕⠝⠎⠂ ⠞⠗⠁⠙⠑ ⠕⠗ ⠏⠗⠕⠋⠑⠎⠎⠊⠕⠝⠁⠇ ⠁⠎⠎⠕⠉⠊⠁⠞⠊⠕⠝⠎⠲

⠠⠫ ⠍ ⠔⠋⠕⠗⠍⠁⠞⠊⠕⠝⠒
⠠⠛⠥⠊⠙⠑ ⠞⠕ ⠽⠗ ⠗⠎ ⠯ ⠗⠑⠎⠏⠕⠝⠎⠊⠃⠊⠇⠭⠊⠑⠎ ⠥⠝ ⠮ ⠠⠓⠥⠍⠁⠝ ⠠⠗⠎ ⠠⠉⠕⠙⠑
⠠⠛⠥⠊⠙⠑⠇⠔⠑⠎ ⠕⠝ ⠙⠑⠧⠑⠇⠕⠏⠔ ⠓⠥⠍⠁⠝ ⠗⠎ ⠏⠕⠇⠊⠉⠊⠑⠎ ⠯ ⠏⠗⠕⠉⠑⠙⠥⠗⠑⠎
⠠⠓⠥⠍⠁⠝ ⠠⠗⠎ ⠠⠉⠕⠙⠑ ⠉⠁⠗⠙⠎

