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
    ';': '⠆', '-': '⠤', "'": '⠄', ' ': ' ',
}

# Multi-cell signs for explicit handling
OPEN_DOUBLE_QUOTE = '⠦' # UEB Open Double Quote
CLOSE_DOUBLE_QUOTE = '⠴' # UEB Close Double Quote
OPEN_PARENTHESIS = '⠐⠣'
CLOSE_PARENTHESIS = '⠐⠜'
FORWARD_SLASH = '⠸⠌'

BRAILLE_INDICATORS = {
    'CAPS': '⠠', 
    'NUM': '⠼',
}
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}

# --- Reverse Maps for Braille-to-Text Conversion ---
REVERSE_LETTER_MAP = {v: k for k, v in BRAILLE_LETTERS.items()}

# Updated Reverse Punctuation Map
REVERSE_PUNCTUATION_MAP = {
    **{v: k for k, v in PUNCTUATION_SIGNS.items()},
    OPEN_DOUBLE_QUOTE: '"', 
    CLOSE_DOUBLE_QUOTE: '"',
    '⠶': '"', # For compatibility with generic double quote (if produced)
    '⠦': '?', # '?'
    '⠖': '!', # '!'
    '⠒': ':', # ':'
    '⠆': ';', # ';'
    '⠲': '.', # '.'
    '⠂': ',', # ','
    '⠤': '-', # '-'
    '⠄': "'", # "'"
}
REVERSE_NUMBER_MAP = {v: k for k, v in NUMBER_MAP.items()}
# ------------------------------------------------------------------

TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')


# --- Core Conversion Functions ---

def text_to_braille(text_input, grade):
    """
    Converts a plain text string to Braille Grade 1 (Uncontracted).
    """
    if grade != BrailleGrade.GRADE_1:
        return "Unsupported Braille Grade."

    tokens = TOKEN_REGEX.findall(text_input)
    braille_output = []
    
    is_quote_open = False 

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
                # Handle specific multi-cell or distinct quotes
                if char == '(':
                    braille_output.append(OPEN_PARENTHESIS)
                elif char == ')':
                    braille_output.append(CLOSE_PARENTHESIS)
                elif char == '/':
                    braille_output.append(FORWARD_SLASH)
                elif char == '"':
                    if not is_quote_open:
                        braille_output.append(OPEN_DOUBLE_QUOTE)
                        is_quote_open = True
                    else:
                        braille_output.append(CLOSE_DOUBLE_QUOTE)
                        is_quote_open = False
                else:
                    # Fallback to single-cell punctuation map
                    braille_output.append(PUNCTUATION_SIGNS.get(char, char))
            continue

        braille_output.append(token)

    return "".join(braille_output)

def braille_to_text(braille_input):
    """
    Converts Braille (Grade 1 only) back to text.
    **FIXED: Numeric mode handling for period (⠲) and comma (⠂) added.**
    """
    text_output = []
    i = 0
    is_num_mode = False
    is_caps_mode = False 
    
    multi_cell_braille = {
        '⠐⠣': '(',   # Open Parenthesis
        '⠐⠜': ')',   # Close Parenthesis
        '⠸⠌': '/',   # Forward Slash
    }
    
    braille_chars = list(braille_input)
    n = len(braille_chars)

    while i < n:
        # Check for multi-cell signs first (up to 2 cells)
        found_multi_cell = False
        for braille_sign, print_char in multi_cell_braille.items():
            sign_len = len(braille_sign)
            if i + sign_len <= n and "".join(braille_chars[i:i+sign_len]) == braille_sign:
                text_output.append(print_char)
                is_num_mode = False 
                is_caps_mode = False
                i += sign_len
                found_multi_cell = True
                break
        
        if found_multi_cell:
            continue
            
        char = braille_chars[i]

        if char == ' ':
            text_output.append(' ')
            is_num_mode = False 
            is_caps_mode = False
            i += 1
            continue

        # Check for indicators
        if char == BRAILLE_INDICATORS['CAPS']: # Capital Indicator (⠠)
            i += 1
            if i < n:
                next_char = braille_chars[i]
                text_output.append(REVERSE_LETTER_MAP.get(next_char, next_char).upper())
                is_num_mode = False 
                is_caps_mode = True 
                i += 1
            else:
                text_output.append('[CAP_IND]') 
            continue

        if char == BRAILLE_INDICATORS['NUM']: # Numeric Indicator (⠼)
            is_num_mode = True
            is_caps_mode = False 
            i += 1
            continue
        
        # --- FIX: Numeric Mode Processing ---
        if is_num_mode:
            # 1. Check for digits first (a-j -> 1-0)
            if char in REVERSE_NUMBER_MAP:
                text_output.append(REVERSE_NUMBER_MAP[char])
                # Numeric mode continues
            # 2. Check for numeric-retaining punctuation (period, comma)
            elif char == '⠲': # period
                text_output.append('.')
                # Numeric mode continues
            elif char == '⠂': # comma
                text_output.append(',')
                # Numeric mode continues
            else:
                # Any other character terminates numeric mode.
                is_num_mode = False
                # Re-evaluate this character in non-numeric mode, so decrement i
                i -= 1 
                
        # Non-numeric mode processing
        else:
            # Check for single-cell braille quotes (⠦ 'open', ⠴ 'close', ⠶ 'generic')
            if char == OPEN_DOUBLE_QUOTE or char == CLOSE_DOUBLE_QUOTE or char == '⠶':
                text_output.append('"')
                is_caps_mode = False 
            
            # Check for letters/punctuation (single cell)
            elif char in REVERSE_LETTER_MAP:
                text_output.append(REVERSE_LETTER_MAP[char])
                is_caps_mode = False
            elif char in REVERSE_PUNCTUATION_MAP:
                text_output.append(REVERSE_PUNCTUATION_MAP[char])
                is_caps_mode = False
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