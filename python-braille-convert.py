# Updated and corrected Python Braille converter script
import sys
import re

# Refined and corrected map for Unified English Braille (UEB) Grade 2.
# Mappings are organized for clarity and logical processing.

# Single-cell letters and basic signs
BRAILLE_LETTERS = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
    'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
    's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵',
}

# Punctuation and indicators
PUNCTUATION_SIGNS = {
    ' ': ' ', '.': '⠲', ',': '⠂', '!': '⠖', '?': '⠦',
    ':': '⠒', ';': '⠐⠆', '-': '⠤',
    '(': '⠣', ')': '⠜', '"': '⠶', "'": '⠄',
}

# Key Braille indicators
BRAILLE_INDICATORS = {
    'CAPS': '⠠',
    'WHOLE_WORD_CAPS': '⠠⠠',
    'NUM': '⠼',
}

# Organize contractions by their rules of use for correct application
# 1. Whole-word contractions (Alphabetical Word Signs & Strong Word Signs)
WHOLE_WORD_CONTRACTIONS = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
    'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
    'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
    's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵', 'and': '⠯', 'for': '⠫', 'of': '⠷', 'the': '⠮', 'with': '⠾',
    'be': '⠐⠃', 'but': '⠃', 'can': '⠉', 'do': '⠙', 'every': '⠑',
    'from': '⠋', 'go': '⠛', 'have': '⠓', 'it': '⠊', 'just': '⠚',
    'knowledge': '⠅', 'like': '⠇', 'more': '⠍', 'not': '⠝',
    'people': '⠏', 'quite': '⠟', 'rather': '⠗', 'so': '⠎', 'that': '⠞',
    'us': '⠥', 'very': '⠧', 'will': '⠺', 'you': '⠽',
    'in': '⠔', 'was': '⠐⠧', 'his': '⠐⠓', 'were': '⠐⠺',
}

# 2. Shortform contractions (stand alone as a whole word)
SHORTFORM_CONTRACTIONS = {
    'about': '⠁⠃', 'above': '⠁⠃⠧', 'according': '⠁⠉⠉', 'after': '⠁⠋', 'again': '⠁⠛',
    'almost': '⠁⠇⠍', 'already': '⠁⠇⠗', 'also': '⠁⠇⠎', 'although': '⠁⠇', 'altogether': '⠁⠇⠞',
    'always': '⠁⠇⠺', 'behind': '⠃⠓', 'below': '⠃⠇', 'beneath': '⠃⠝', 'beside': '⠃⠎',
    'braille': '⠃⠗⠇', 'character': '⠉⠓⠁', 'children': '⠉⠓⠣', 'could': '⠉⠙', 'first': '⠋⠗',
    'great': '⠛⠗', 'had': '⠓⠙', 'immediate': '⠔⠍', 'little': '⠇', 'made': '⠍⠙', 'many': '⠍⠁',
    'must': '⠍⠎', 'necessary': '⠝⠑⠉', 'neither': '⠝⠗', 'one': '⠕⠝', 'part': '⠏⠁',
    'quick': '⠟⠅', 'right': '⠗⠎', 'said': '⠎⠙', 'some': '⠎⠍',
    'spirit': '⠎⠏', 'such': '⠎⠥', 'their': '⠹⠗', 'these': '⠹⠎', 'this': '⠹',
    'those': '⠹⠎', 'through': '⠹⠗', 'time': '⠞⠊', 'under': '⠥⠝', 'upon': '⠥⠏',
    'where': '⠱', 'which': '⠱', 'who': '⠱', 'whose': '⠱⠎', 'word': '⠺⠙', 'work': '⠺⠅',
    'world': '⠺⠇', 'would': '⠺⠙', 'young': '⠽⠛', 'your': '⠽⠗',
}

# 3. Strong Group Signs (can be anywhere in a word)
STRONG_GROUP_SIGNS = {
    'ch': '⠡', 'gh': '⠛⠓', 'sh': '⠩', 'th': '⠹', 'wh': '⠱',
    'ou': '⠳', 'ow': '⠪', 'st': '⠌', 'en': '⠢', 'ff': '⠖',
}

# 4. Final-letter contractions (must be at the end of a word)
FINAL_LETTER_CONTRACTIONS = {
    'ing': '⠔', 'ar': '⠜', 'ed': '⠫', 'er': '⠻',
    'tion': '⠞⠊⠕⠝', 'sion': '⠎⠊⠕⠝', 'ful': '⠋⠥⠇', 'ness': '⠝⠑⠎⠎',
    'less': '⠇⠎', 'ence': '⠂⠝⠉', 'ment': '⠍⠢',
}

# 5. Initial-letter contractions (must be at the beginning of a word)
INITIAL_LETTER_CONTRACTIONS = {
    'child': '⠉⠓⠙', 'day': '⠙', 'ever': '⠑⠧', 'here': '⠓⠑',
    'name': '⠝⠁⠍⠑', 'one': '⠕⠝⠑', 'shall': '⠩', 'that': '⠹',
    'these': '⠹⠎⠑', 'those': '⠹⠎⠑', 'through': '⠹⠗', 'which': '⠱',
    'with': '⠾', 'would': '⠺⠙', 'you': '⠽',
}

# Numeric mapping
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}

# Compile regex for tokenization
TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')

def text_to_braille(text_input):
    """
    Converts a string of English text to Braille using a precedence-based approach.
    """
    tokens = TOKEN_REGEX.findall(text_input)
    braille_output = []

    # Combine all contraction dictionaries into a single list of (text, braille) pairs
    # and sort by the length of the English text in descending order for greedy matching.
    all_contractions = []
    all_contractions.extend(WHOLE_WORD_CONTRACTIONS.items())
    all_contractions.extend(SHORTFORM_CONTRACTIONS.items())
    all_contractions.extend(FINAL_LETTER_CONTRACTIONS.items())
    all_contractions.extend(STRONG_GROUP_SIGNS.items())
    all_contractions.extend(INITIAL_LETTER_CONTRACTIONS.items())

    # Sort by length of the English part, descending
    all_contractions.sort(key=lambda x: len(x[0]), reverse=True)
    
    # Create a set for quick lookup of word-ending contractions
    final_contractions = set(FINAL_LETTER_CONTRACTIONS.keys())
    
    # Create a set for quick lookup of strong group contractions
    strong_group_signs = set(STRONG_GROUP_SIGNS.keys())

    def convert_word(word):
        braille_word_output = []
        i = 0
        while i < len(word):
            found_match = False
            remaining = word[i:]

            # Prioritize longer contractions first.
            
            # 1. Final contractions check
            if any(remaining.endswith(fc) for fc in final_contractions) and i == len(word) - len(remaining):
                braille_word_output.append(convert_word(word[:i]))
                for fc, b in FINAL_LETTER_CONTRACTIONS.items():
                    if remaining.endswith(fc):
                        braille_word_output.append(b)
                        break
                i = len(word)
                found_match = True
                break
            
            # 2. Strong group contractions check (anywhere in word)
            for group, braille in sorted(STRONG_GROUP_SIGNS.items(), key=lambda x: len(x[0]), reverse=True):
                if remaining.startswith(group):
                    braille_word_output.append(braille)
                    i += len(group)
                    found_match = True
                    break
            if found_match:
                continue

            # Fallback to single letter
            braille_word_output.append(BRAILLE_LETTERS.get(word[i], word[i]))
            i += 1
            
        return "".join(braille_word_output)

    for token in tokens:
        if token.isspace() or re.match(r'^[^\w\s]+$', token):
            for char in token:
                braille_output.append(PUNCTUATION_SIGNS.get(char, char))
        elif token.isdigit():
            braille_output.append(BRAILLE_INDICATORS['NUM'])
            for digit in token:
                braille_output.append(NUMBER_MAP.get(digit, ''))
        else:
            braille_word = []
            lower_token = token.lower()
            is_all_caps = token.isupper() and len(token) > 1
            is_initial_caps = token[0].isupper()

            if is_all_caps:
                braille_word.append(BRAILLE_INDICATORS['WHOLE_WORD_CAPS'])
            elif is_initial_caps:
                braille_word.append(BRAILLE_INDICATORS['CAPS'])

            # Rule 1: Check for whole-word and shortform contractions first
            if lower_token in WHOLE_WORD_CONTRACTIONS:
                braille_word.append(WHOLE_WORD_CONTRACTIONS[lower_token])
            elif lower_token in SHORTFORM_CONTRACTIONS:
                braille_word.append(SHORTFORM_CONTRACTIONS[lower_token])
            else:
                braille_word.append(convert_word(lower_token))

            braille_output.append("".join(braille_word))

    return "".join(braille_output)


def braille_to_text(braille_input):
    """
    Converts Braille to English text with improved logic and a corrected reverse map.
    """
    english_output = []
    i = 0
    capitalize_next = False
    capitalize_whole_word = False
    in_numeric_mode = False

    # A single, correct, and comprehensive Braille-to-English map that prioritizes longer patterns
    reverse_map = {
        '⠠⠠': ('_WHOLE_WORD_CAPS', 2), '⠠': ('_CAPS', 1), '⠼': ('_NUM', 1),
        **{v: (k, 1) for k, v in WHOLE_WORD_CONTRACTIONS.items()},
        **{v: (k, 1) for k, v in SHORTFORM_CONTRACTIONS.items()},
        **{v: (k, 1) for k, v in STRONG_GROUP_SIGNS.items()},
        **{v: (k, 1) for k, v in FINAL_LETTER_CONTRACTIONS.items()},
        **{v: (k, 1) for k, v in BRAILLE_LETTERS.items()},
        **{v: (k, 1) for k, v in PUNCTUATION_SIGNS.items()},
    }
    
    # Remove duplicate values (e.g., '⠁' for 'a' and 'and') by prioritizing longer keys.
    # This is a critical step to ensure correct reverse mapping.
    reverse_map_unique = {}
    for braille_char, (english_text, length) in reverse_map.items():
        # Prioritize longer Braille patterns (e.g., '⠐⠃' over '⠃')
        if braille_char not in reverse_map_unique or len(english_text) > len(reverse_map_unique[braille_char][0]):
            reverse_map_unique[braille_char] = (english_text, length)
            
    # Add number mappings to the unique reverse map
    for digit, braille_char in NUMBER_MAP.items():
        reverse_map_unique[braille_char] = (digit, 1)

    sorted_patterns = sorted(reverse_map_unique.keys(), key=len, reverse=True)

    while i < len(braille_input):
        current_braille_part = braille_input[i:]
        found_match = False
        
        # Check for indicators first
        if current_braille_part.startswith(BRAILLE_INDICATORS['WHOLE_WORD_CAPS']):
            capitalize_whole_word = True
            i += len(BRAILLE_INDICATORS['WHOLE_WORD_CAPS'])
            found_match = True
        elif current_braille_part.startswith(BRAILLE_INDICATORS['CAPS']):
            capitalize_next = True
            i += len(BRAILLE_INDICATORS['CAPS'])
            found_match = True
        elif current_braille_part.startswith(BRAILLE_INDICATORS['NUM']):
            in_numeric_mode = True
            i += len(BRAILLE_INDICATORS['NUM'])
            found_match = True
        
        if found_match: continue

        # Handle numeric patterns
        if in_numeric_mode:
            found_num = False
            for digit, braille_char in NUMBER_MAP.items():
                if current_braille_part.startswith(braille_char):
                    english_output.append(digit)
                    i += len(braille_char)
                    found_num = True
                    break
            
            # Exit numeric mode at a non-numeric braille character or space
            if not found_num or braille_input[i] == ' ':
                in_numeric_mode = False
            continue

        # Match against sorted patterns (longer first)
        for pattern in sorted_patterns:
            if current_braille_part.startswith(pattern):
                english_part, _ = reverse_map_unique[pattern]
                
                if english_part == ' ':
                    capitalize_whole_word = False
                
                # Apply capitalization
                if capitalize_next:
                    english_output.append(english_part.capitalize())
                    capitalize_next = False
                elif capitalize_whole_word:
                    english_output.append(english_part.upper())
                else:
                    english_output.append(english_part)
                
                i += len(pattern)
                found_match = True
                break
        
        if not found_match:
            english_output.append(current_braille_part[0])
            i += 1

    return "".join(english_output).strip()


def main():
    """
    Main function to handle command-line arguments and file operations.
    """
    if len(sys.argv) < 3:
        print("Usage:")
        print("  To convert a file: python braille_converter.py [file_path] [to_braille|to_text]")
        print("  Example: python braille_converter.py sample.txt to_braille")
        return

    file_path = sys.argv[1]
    direction = sys.argv[2]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    print(f"--- Original Content from '{file_path}' ---")
    print(content)
    print("-" * 30)

    if direction == "to_braille":
        converted_content = text_to_braille(content)
        print("--- Converted to Braille ---")
        print(converted_content)
    elif direction == "to_text":
        converted_content = braille_to_text(content)
        print("--- Converted to English Text ---")
        print(converted_content)
    else:
        print("Error: Invalid conversion direction. Use 'to_braille' or 'to_text'.")

if __name__ == "__main__":
    main()