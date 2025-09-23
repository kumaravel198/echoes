# Echoes-Insights
Echoes &amp; Insights is an initiative using Google Gemini to make digital information accessible to everyone. The project creates high-quality content like automatic closed captions for the Deaf and hard of hearing, and braille transcriptions for those with low vision, building a more equitable digital landscape.

## Python Braille Converter

A Python script that converts English text to Unified English Braille (UEB) and back again. The script is designed to handle a variety of text features including contractions, capitalization, punctuation, and numbers.

## Features

- **Bidirectional Conversion**: Converts text to Braille and Braille back to text.
- **UEB Grade 2 Support**: Implements a wide range of contractions and rules from Unified English Braille Grade 2.
- **Contraction Handling**: Accurately processes whole-word, shortform, and group sign contractions to produce more efficient Braille output.
- **Punctuation and Numbers**: Correctly translates common punctuation and numerical digits using the Braille numeric indicator.
- **Capitalization Rules**: Applies capital signs for single capitalized letters and a double capital sign for fully capitalized words.
- **Command-line Interface**: Easy to use via command-line arguments for file-based conversion.

## How It Works

The script operates in two main modes: `text_to_braille` and `braille_to_text`.

- **`text_to_braille`**: This function tokenizes the input text into words, numbers, and punctuation. It applies a rule-based system, prioritizing longer contractions first to ensure the most concise Braille representation possible. It handles capitalization by inserting the appropriate indicator (`⠠` for single capital, `⠠⠠` for whole words).

- **`braille_to_text`**: This function works in reverse, iterating through the Braille input and matching patterns against a comprehensive reverse map. It correctly interprets indicators for capitalization and numbers to reconstruct the original English text. The reverse map is carefully ordered to handle multi-cell Braille patterns before single-cell ones, preventing incorrect translations.

## Usage

The script is a command-line tool. You must provide a file path and a conversion direction as arguments.

### **To convert a text file to Braille:**

```bash
python braille_converter.py [path_to_your_text_file] to_braille
```
## Docker Container Usage

Coming soon!
