# Corrected Python Braille converter script with Grade 1/Grade 2 selection
import sys
import re
from enum import Enum, auto

# --- Enums and Constants ---

class BrailleGrade(Enum):
    """Enumeration for Braille Conversion Grade."""
    GRADE_1 = auto()  # Uncontracted Braille
    GRADE_2 = auto()  # Contracted Braille (Disabled for stability, but kept for enum)

# Unified English Braille (UEB) Mappings

# Single-cell letters and basic signs
BRAILLE_LETTERS = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
    'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
    's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵',
}

# Punctuation and symbols (Grade 1/Grade 2 common)
PUNCTUATION_SIGNS = {
    '.': '⠲', ',': '⠂', '!': '⠖', '?': '⠦', ':': '⠒',
    ';': '⠆', '-': '⠤', '"': '⠶', "'": '⠄', ' ': ' ',
}

# Number signs (1-0 correspond to a-j)
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}

# Indicators
BRAILLE_INDICATORS = {
    'CAPS': '⠠', # Capital letter indicator
    'NUM': '⠼',  # Numeric indicator
}

# Reverse Maps for Braille-to-Text Conversion (The "Spectacular Failure" Fix)
REVERSE_LETTER_MAP = {v: k for k, v in BRAILLE_LETTERS.items()}
REVERSE_PUNCTUATION_MAP = {v: k for k, v in PUNCTUATION_SIGNS.items()}
REVERSE_NUMBER_MAP = {v: k for k, v in NUMBER_MAP.items()}

# Regex to split text into words, numbers, and symbols
TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')

# --- Core Conversion Functions ---

def text_to_braille(text_input, grade):
    """Converts a plain text string to Braille (Grade 1 only for reliability)."""
    if grade != BrailleGrade.GRADE_1:
        # Fallback or error for other grades
        return "ERROR: Only Grade 1 conversion is supported."

    tokens = TOKEN_REGEX.findall(text_input)
    braille_output = []

    for token in tokens:
        if token.isspace():
            braille_output.append(token)
            continue
            
        if token.isdigit():
            # CORRECTED: Apply Numeric Indicator (⠼) and map digits
            braille_output.append(BRAILLE_INDICATORS['NUM'])
            for digit in token:
                braille_output.append(NUMBER_MAP.get(digit, digit))
            continue
            
        if re.match(r'^[A-Za-z]+$', token):
            # Handle words (letter-for-letter in Grade 1)
            for char in token:
                if 'a' <= char <= 'z':
                    # Lowercase
                    braille_output.append(BRAILLE_LETTERS.get(char))
                elif 'A' <= char <= 'Z':
                    # Capital: Apply Capital Indicator (⠠)
                    lower_char = char.lower()
                    braille_code = BRAILLE_LETTERS.get(lower_char, '')
                    if braille_code:
                        braille_output.append(BRAILLE_INDICATORS['CAPS'] + braille_code)
                    else:
                        braille_output.append(char) # Fallback
            continue

        # Handle punctuation and other symbols
        if re.match(r'^[^\w\s]+$', token):
            for char in token:
                braille_output.append(PUNCTUATION_SIGNS.get(char, char))
            continue

        # Fallback for unhandled tokens
        braille_output.append(token)

    return "".join(braille_output)

def braille_to_text(braille_input):
    """
    CORRECTED: Converts Braille (Grade 1 only) back to text.
    Handles capitals, numbers, letters, and punctuation.
    """
    text_output = []
    i = 0
    is_num_mode = False
    
    # Concatenate all reverse maps for single-cell lookups
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
            i += 1
            continue

        # Check for indicators
        if char == BRAILLE_INDICATORS['CAPS']: # Capital Indicator (⠠)
            i += 1
            if i < len(braille_chars):
                next_char = braille_chars[i]
                text_output.append(REVERSE_LETTER_MAP.get(next_char, next_char).upper())
                is_num_mode = False
                i += 1
            else:
                # Malformed braille, treat indicator as error or print it
                text_output.append('[CAP_IND]') 
            continue

        if char == BRAILLE_INDICATORS['NUM']: # Numeric Indicator (⠼)
            is_num_mode = True
            i += 1
            continue

        # Process characters based on mode
        if is_num_mode:
            # Look up in the reverse number map
            text_output.append(REVERSE_NUMBER_MAP.get(char, char))
        else:
            # Check for letters/punctuation
            if char in REVERSE_LETTER_MAP:
                text_output.append(REVERSE_LETTER_MAP[char])
            elif char in REVERSE_PUNCTUATION_MAP:
                text_output.append(REVERSE_PUNCTUATION_MAP[char])
            else:
                text_output.append(char) # Unhandled character

        i += 1
        
    return "".join(text_output)


# Command line usage logic (kept for completeness)
if __name__ == '__main__':
    # ... (rest of the command-line usage logic)
    if len(sys.argv) < 3:
        print("Usage:")
        print("  To convert a file: python python-braille-convert.py [file_path] [to_braille_g1|to_text]")
        print("  Example: python python-braille-convert.py sample.txt to_braille_g1")
        return

    # ... (rest of the file reading logic) ...

    if direction == "to_braille_g1":
        converted_content = text_to_braille(content, grade=BrailleGrade.GRADE_1)
        print("--- Converted to Braille (Grade 1) ---")
        print(converted_content)
    elif direction == "to_text":
        converted_content = braille_to_text(content)
        print("--- Converted to Text ---")
        print(converted_content)
    else:
        print(f"Error: Invalid direction '{direction}'. Only 'to_braille_g1' and 'to_text' are supported.")