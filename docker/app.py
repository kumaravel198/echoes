# app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import re
from enum import Enum, auto

# --- Enums and Mappings ---
class BrailleGrade(Enum):
    GRADE_1 = auto()
    GRADE_2 = auto()

# Unified English Braille (UEB) Mappings (Subset from python-braille-convert.py)
BRAILLE_LETTERS = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
    'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
    's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵',
}
PUNCTUATION_SIGNS = {
    '.': '⠲', ',': '⠂', '!': '⠖', '?': '⠦', ':': '⠒',
    ';': '⠆', '-': '⠤', '"': '⠶', "'": '⠄', ' ': ' ',
}
BRAILLE_INDICATORS = {
    'CAPS': '⠠', 
    'NUM': '⠼',
}
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}

# --- Reverse Maps for Braille-to-Text Conversion (THE FIX) ---
REVERSE_LETTER_MAP = {v: k for k, v in BRAILLE_LETTERS.items()}
REVERSE_PUNCTUATION_MAP = {v: k for k, v in PUNCTUATION_SIGNS.items()}
REVERSE_NUMBER_MAP = {v: k for k, v in NUMBER_MAP.items()}
# ------------------------------------------------------------------

TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')


# --- Core Conversion Functions (Copied from python-braille-convert.py) ---

def text_to_braille(text_input, grade):
    """
    Converts a plain text string to Braille Grade 1 (Uncontracted).
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
            braille_output.append(BRAILLE_INDICATORS['NUM'])
            for digit in token:
                braille_output.append(NUMBER_MAP.get(digit, digit))
            continue
            
        if re.match(r'^[A-Za-z]+$', token):
            for char in token:
                if 'a' <= char <= 'z':
                    braille_output.append(BRAILLE_LETTERS.get(char))
                elif 'A' <= char <= 'Z':
                    lower_char = char.lower()
                    braille_code = BRAILLE_LETTERS.get(lower_char, '')
                    if braille_code:
                        braille_output.append(BRAILLE_INDICATORS['CAPS'] + braille_code)
                    else:
                        braille_output.append(char)
            continue

        if re.match(r'^[^\w\s]+$', token):
            for char in token:
                braille_output.append(PUNCTUATION_SIGNS.get(char, char))
            continue

        braille_output.append(token)

    return "".join(braille_output)

def braille_to_text(braille_input):
    """
    Converts Braille (Grade 1 only) back to text.
    Handles capitals, numbers, letters, and punctuation.
    """
    text_output = []
    i = 0
    is_num_mode = False
    is_caps_mode = False # Added for consistency with text_to_braille indicator check
    
    # Concatenate all reverse maps for single-cell lookups (Simplified lookup)
    all_reverse_maps = {
        **REVERSE_LETTER_MAP, 
        **REVERSE_PUNCTUATION_MAP, 
        **REVERSE_NUMBER_MAP
    }
    
    braille_chars = list(braille_input)

    while i < len(braille_chars):
        char = braille_chars[i]

        if char == ' ':
            text_output.append(' ')
            is_num_mode = False # Space breaks numeric mode
            is_caps_mode = False
            i += 1
            continue

        # Check for indicators
        if char == BRAILLE_INDICATORS['CAPS']: # Capital Indicator (⠠)
            i += 1
            if i < len(braille_chars):
                next_char = braille_chars[i]
                # Look up the letter, capitalize it, and append
                text_output.append(REVERSE_LETTER_MAP.get(next_char, next_char).upper())
                is_num_mode = False # A capital letter is not a number
                i += 1
            else:
                text_output.append('[CAP_IND]') 
            continue

        if char == BRAILLE_INDICATORS['NUM']: # Numeric Indicator (⠼)
            is_num_mode = True
            is_caps_mode = False # Numbers override capitalization
            i += 1
            continue

        # Process characters based on mode
        if is_num_mode:
            # Look up in the reverse number map
            text_output.append(REVERSE_NUMBER_MAP.get(char, char))
            # If the character is not a number, numeric mode is broken by the end of the word/token in original script, 
            # but for robustness, a space is the primary break. Keep going until a space or another indicator.
        else:
            # Check for letters/punctuation
            if char in REVERSE_LETTER_MAP:
                text_output.append(REVERSE_LETTER_MAP[char])
            elif char in REVERSE_PUNCTUATION_MAP:
                text_output.append(REVERSE_PUNCTUATION_MAP[char])
                is_caps_mode = False # Punctuation breaks capitalization
            else:
                text_output.append(char) # Unhandled character

        i += 1
        
    return "".join(text_output)


# --- Flask Application Setup ---

app = Flask(__name__, static_folder='static') 
CORS(app) 

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """Serves the HTML frontend."""
    if path == "" or os.path.exists(os.path.join(app.static_folder, path)):
        if path == "" or not os.path.isfile(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return send_from_directory(app.static_folder, path)
    return "Not Found", 404

                                                                                                                                                                            
@app.route('/convert', methods=['POST'])
def convert():
    """API endpoint to handle Braille conversion."""
    data = request.get_json()
    input_text = data.get('text', '')
    conversion_type = data.get('conversion_type', 'to_braille_g1')
    
    converted_text = ""
    try:
        if conversion_type == "to_braille_g1":
            converted_text = text_to_braille(input_text, grade=BrailleGrade.GRADE_1)
        elif conversion_type == "to_text":
            converted_text = braille_to_text(input_text)
        else:
            return jsonify({"error": "Invalid conversion type. Only Grade 1 and Text conversion are supported."}), 400

        return jsonify({"result": converted_text})

    except Exception as e:
        print(f"Conversion error: {e}", file=sys.stderr)
        return jsonify({"error": "An internal conversion error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)