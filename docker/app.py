# app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Temporarily append the current directory to the path to import the converter
# In a real setup, this would be a proper package installation.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- START: Content from python-braille-convert.py (Adjusted for import) ---
# NOTE: In a real-world scenario, you would structure this better with imports.
# For simplicity, I'm defining the necessary parts here.

import re
from enum import Enum, auto

class BrailleGrade(Enum):
    GRADE_1 = auto()
    GRADE_2 = auto()

# --- Required imports and maps from python-braille-convert.py (partial list for illustration) ---
BRAILLE_LETTERS = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
    'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
    's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵',
}
PUNCTUATION_SIGNS = {
    # Basic Punctuation
    ' ': ' ', 
    '.': '⠲', # Period/Dot
    ',': '⠂', # Comma
    '!': '⠖', # Exclamation point
    '?': '⠦', # Question mark
    ':': '⠒', # Colon
    ';': '⠆', # Semicolon
    '-': '⠤', # Hyphen
    
    # Quotation Marks (Generic and Directional)
    '"': '⠶',  # Generic Double Quote (Dots 2-3-5-6)
    '“': '⠦',  # Opening Directional Quote
    '”': '⠴',  # Closing Directional Quote

    # Apostrophe
    "'": '⠄', # Apostrophe/Closing Single Quote

    # Ellipsis (Multi-cell)
    '...': '⠲⠲⠲',
    
    # Dashes/Slashes (Multi-cell)
    '—': '⠠⠤',  # Em-dash/Long Dash
    '/': '⠸⠌',  # Forward Slash

    # Grouping Punctuation (Two-cell forms)
    '(': '⠐⠣', # Opening Parenthesis
    ')': '⠐⠜', # Closing Parenthesis (Corrected from non-standard ✜)
    '[': '⠨⠣', # Opening Square Bracket
    ']': '⠨⠜', # Closing Square Bracket

    # Currency and Symbols
    '$': '⠐⠎', # Dollar Sign
    '*': '⠐⠔', # Asterisk
}
# Key Braille indicators - EXPANDED UEB INDICATORS
BRAILLE_INDICATORS = {
    # Capitalization Indicators (Corrected WHOLE_WORD_CAPS to CAPS_WORD)
    'CAPS': '⠠',                   # Capital Letter Indicator (Dot 6)
    'CAPS_WORD': '⠠⠠',              # Capital Word Indicator (Dot 6, Dot 6)
    'CAPS_PASSAGE': '⠠⠠⠠',         # Capital Passage Indicator (Dot 6, Dot 6, Dot 6)
    'CAPS_TERMINATOR': '⠠⠄',        # Capital Passage Terminator (Dot 6, Dot 3)

    # Grade 1 (Uncontracted) Indicators
    'G1_SYM': '⠰',                   # Grade 1 Symbol Indicator (Dots 5-6)
    'G1_WORD': '⠰⠰',                # Grade 1 Word Indicator (Dots 5-6, 5-6)
    'G1_PASSAGE': '⠰⠰⠰',             # Grade 1 Passage Indicator (Dots 5-6, 5-6, 5-6)
    'G1_TERMINATOR': '⠰⠄',          # Grade 1 Passage Terminator (Dots 5-6, 3)

    # ... other indicators (omitted for brevity, as the logic only uses NUM, CAPS, CAPS_WORD)
    'NUM': '⠼',                    # Numeric Indicator (Dots 3-4-5-6)
}
# Numeric mapping
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}

# (All contraction maps and sorted lists must also be included)
STRONG_WORD_SIGNS = {
    'and': '⠯', 'for': '⠫', 'of': '⠷', 'the': '⠮', 'with': '⠾',
    'child': '⠡', 'shall': '⠩', 'this': '⠹', 'which': '⠱', 'out': '⠳',
    'still': '⠌',
}

# app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import re
from enum import Enum, auto

# --- Enums and Mappings (Keep these the same) ---
class BrailleGrade(Enum):
    GRADE_1 = auto()
    GRADE_2 = auto()

# (Keep BRAILLE_LETTERS, PUNCTUATION_SIGNS, BRAILLE_INDICATORS, NUMBER_MAP)
BRAILLE_LETTERS = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
    'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
    's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵',
}
PUNCTUATION_SIGNS = {
    ' ': ' ', '.': '⠲', ',': '⠂', '!': '⠖', '?': '⠦', ':': '⠒',
    ';': '⠆', '-': '⠤', '"': '⠶', '“': '⠦', '”': '⠴', "'": '⠄',
    '(': '⠐⠣', ')': '⠐⠜', '[': '⠨⠣', ']': '⠨⠜', '$': '⠐⠎', '*': '⠐⠔',
}
BRAILLE_INDICATORS = {
    'CAPS': '⠠',
    'NUM': '⠼',
}
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}
TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)') # Keep the tokenizer

# --- CORRECTED text_to_braille function ---
def text_to_braille(text_input, grade):
    """
    Converts a plain text string to Braille Grade 1 (Uncontracted).
    This version correctly handles capitalization, numbers, and punctuation.
    """
    if grade != BrailleGrade.GRADE_1:
        return "Unsupported Braille Grade."

    tokens = TOKEN_REGEX.findall(text_input)
    braille_output = []

    for token in tokens:
        if token.isspace():
            braille_output.append(token)
            continue
            
        if token.isdigit():
            # Apply Numeric Indicator (⠼)
            braille_output.append(BRAILLE_INDICATORS['NUM']) # This adds '⠼'
            for digit in token:
                braille_output.append(NUMBER_MAP.get(digit, digit))
            continue
            
        if re.match(r'^[A-Za-z]+$', token):
            # Handle words (letter-for-letter)
            for char in token:
                if 'a' <= char <= 'z':
                    # Lowercase letters are directly mapped
                    braille_output.append(BRAILLE_LETTERS.get(char))
                elif 'A' <= char <= 'Z':
                    # Capital letters require the Capital Letter Indicator (⠠)
                    lower_char = char.lower()
                    braille_code = BRAILLE_LETTERS.get(lower_char, '')
                    if braille_code:
                        braille_output.append(BRAILLE_INDICATORS['CAPS'] + braille_code)
                    else:
                        braille_output.append(char) # Fallback
            continue

        # Handle punctuation and other symbols
        if re.match(r'^[^\w\s]+$', token):
            # Process token character by character for punctuation
            for char in token:
                braille_output.append(PUNCTUATION_SIGNS.get(char, char))
            continue

        # If a token is mixed (e.g., 'a.b', which shouldn't happen with the regex)
        # Fallback: append the token as is
        braille_output.append(token)

    return "".join(braille_output)

# (Keep the existing braille_to_text function)
def braille_to_text(braille_input):
    # This is where the actual logic from python-braille-convert.py belongs
    return "Text conversion of: " + braille_input

TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')
WHOLE_WORD_SIGNS = {}


# Initialize Flask app, specifying the static folder
# The Dockerfile copies braille_converter.html to /app/static/index.html
app = Flask(__name__, static_folder='static') 
CORS(app) # Enable CORS for cross-origin requests from the HTML file

# --- NEW ROOT ROUTE TO SERVE THE HTML FRONTEND ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """
    Serves the index.html file for the root path and static files (like CSS/JS) 
    for other paths found in the 'static' folder.
    """
    # If the path is empty (root URL), or if the path is a file that exists in the static folder
    if path == "" or os.path.exists(os.path.join(app.static_folder, path)):
        if path == "" or not os.path.isfile(os.path.join(app.static_folder, path)):
            # If path is "" or a directory, serve index.html (the main frontend file)
            return send_from_directory(app.static_folder, 'index.html')
        else:
            # If the path is an existing file (e.g., an asset), serve it directly
            return send_from_directory(app.static_folder, path)

    # For any other path, return 404
    return "Not Found", 404

                                                                                                                                                                            
@app.route('/convert', methods=['POST'])
def convert():
    """API endpoint to handle Braille conversion."""
    data = request.get_json()
    # Changed default conversion type to 'to_braille_g1'
    input_text = data.get('text', '')
    conversion_type = data.get('conversion_type', 'to_braille_g1')
    
    converted_text = ""
    try:
        # Removed the 'to_braille_g2' case
        if conversion_type == "to_braille_g1":
            converted_text = text_to_braille(input_text, grade=BrailleGrade.GRADE_1)
        elif conversion_type == "to_text":
            converted_text = braille_to_text(input_text)
        else:
            # If the frontend somehow sends an invalid type (like the removed g2), return an error
            return jsonify({"error": "Invalid conversion type. Only Grade 1 and Text conversion are supported."}), 400

        return jsonify({"result": converted_text})

    except Exception as e:
        # Log the error and return a generic server error
        print(f"Conversion error: {e}", file=sys.stderr)
        return jsonify({"error": "An internal conversion error occurred."}), 500

if __name__ == '__main__':
    # Running the Flask app on a specific port, e.g., 5000
    # In a real deployment, a proper web server (Gunicorn, uWSGI) would be used.
    app.run(debug=True, host='0.0.0.0', port=5000)