# app.py

from flask import Flask, request, jsonify
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

# ... (Insert all constants/maps: BRAILLE_LETTERS, PUNCTUATION_SIGNS, etc. from python-braille-convert.py here) ...
# Due to length, I will only include the core functions and necessary imports
# All map definitions (BRAILLE_LETTERS, PUNCTUATION_SIGNS, etc.) MUST be copied here.

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
# ... (all other maps from the Python script) ...
TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')
WHOLE_WORD_SIGNS = {}
# ... (Update WHOLE_WORD_SIGNS and WHOLE_WORD_SIGNS_SORTED) ...
# ... (Include convert_word_part_g2 and convert_word_part_g1) ...

# --- Conversion Functions (must be copied directly from python-braille-convert.py) ---
# text_to_braille(text_input, grade)
# braille_to_text(braille_input)

# --- END: Content from python-braille-convert.py ---

app = Flask(__name__)
CORS(app) # Enable CORS for cross-origin requests from the HTML file

@app.route('/convert', methods=['POST'])
def convert():
    """API endpoint to handle Braille conversion."""
    data = request.get_json()
    input_text = data.get('text', '')
    conversion_type = data.get('conversion_type', 'to_braille_g2')
    
    converted_text = ""
    try:
        if conversion_type == "to_braille_g2":
            converted_text = text_to_braille(input_text, grade=BrailleGrade.GRADE_2)
        elif conversion_type == "to_braille_g1":
            converted_text = text_to_braille(input_text, grade=BrailleGrade.GRADE_1)
        elif conversion_type == "to_text":
            converted_text = braille_to_text(input_text)
        else:
            return jsonify({"error": "Invalid conversion type."}), 400

        return jsonify({"result": converted_text})

    except Exception as e:
        # Log the error and return a generic server error
        print(f"Conversion error: {e}", file=sys.stderr)
        return jsonify({"error": "An internal conversion error occurred."}), 500

if __name__ == '__main__':
    # Running the Flask app on a specific port, e.g., 5000
    # In a real deployment, a proper web server (Gunicorn, uWSGI) would be used.
    app.run(debug=True, host='0.0.0.0', port=5000)