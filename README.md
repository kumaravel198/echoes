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

The time it takes to learn Grade 2 braille varies significantly from person to person, as it depends on factors like age, motivation, and the amount of time dedicated to practice.

Here are some general estimates and insights from various sources:

For adults: Learning contracted (Grade 2) braille can take over a year to learn fluently. Some courses, like those offered by CNIB, are designed to be completed within 12 months.

For children: Children can often learn braille in the same amount of time it takes a sighted child to learn to read, assuming consistent practice. One source suggests that learning Grade 1 braille can take 6-8 months, while Grade 2 can take about 18 months.


Practice is key: The key to fluency is consistent, daily practice. Many experienced braille readers emphasize that simply knowing the contractions isn't enough; real-world practice with books, bank statements, and other materials is what truly builds fluency.

Learning Grade 1 first: It's often recommended to learn uncontracted (Grade 1) braille first, as Grade 2 is a more complex system with contractions that serve as a type of shorthand.

In summary, while there is no single "average" number, a motivated adult or child who practices regularly can expect to spend at least a year, and potentially more, to become fluent in Grade 2 braille.

Legal documents produced in Canada after September 8, 2022, that still use "Regina" instead of "Rex" would not be invalid, but they are technically incorrect and could be subject to administrative delays.
Here's a breakdown of the effects:

Automatic Deemed Amendment: The legal system in Canada is designed to prevent a disruption of government and legal proceedings upon the death of the monarch. The principle of the "Crown as a corporation sole" means that the institution of the Crown continues uninterrupted. In practice, this means that references to "The Queen" or "Regina" in statutes and legal documents are automatically interpreted as "The King" or "Rex." Some courts have issued blanket orders to this effect, meaning that a document does not need to be refiled or amended just because it uses the old terminology.

Administrative Grace Period: Many courts, law firms, and government bodies recognized that this transition would not be instantaneous. They have implemented a grace period during which documents using "Regina" would still be accepted. However, this is not a permanent solution, and eventually, documents with the outdated term may be rejected or returned for correction.
Best Practice and Professionalism: While using "Regina" may not invalidate a document, it is no longer the proper legal terminology. Legal professionals are expected to use the correct and current terms. Continued use of "Regina" could be seen as a sign of inattention to detail or a lack of understanding of the current legal landscape, which could be an issue in a professional context.

Specific Examples:
Case Citations: While older cases will always be cited as "Regina v. [defendant]," any new criminal proceedings initiated after September 8, 2022, should be styled as "Rex v. [defendant]."
Court Names: Provinces like Alberta and New Brunswick have officially renamed their courts from the "Court of Queen's Bench" to the "Court of King's Bench." Any new filings should reflect this change.
Lawyer Titles: The designation "Queen's Counsel" (QC) has automatically become "King's Counsel" (KC). While existing letters patent do not need to be reissued, lawyers are expected to update their business cards, letterheads, and other professional materials.
In summary, while there's a strong legal basis for the validity of documents still using "Regina," the best and proper course of action for any legal document created after the date of the Queen's death is to use the correct term, "Rex."
