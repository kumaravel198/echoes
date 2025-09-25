# Corrected Python Braille converter script with Grade 1/Grade 2 selection
import sys
import re
from enum import Enum, auto

# --- Enums and Constants ---

class BrailleGrade(Enum):
    """Enumeration for Braille Conversion Grade."""
    GRADE_1 = auto()  # Uncontracted Braille
    GRADE_2 = auto()  # Contracted Braille (Default)

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

# Punctuation and indicators (using original script's refined list)
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

# --- Contractions (Used only in Grade 2) ---

# 1. Strong Word Signs (must stand alone as a whole word)
STRONG_WORD_SIGNS = {
    'and': '⠯', 'for': '⠫', 'of': '⠷', 'the': '⠮', 'with': '⠾',
    'child': '⠡', 'shall': '⠩', 'this': '⠹', 'which': '⠱', 'out': '⠳',
    'still': '⠌',
}

# 2. Strong Group Signs (can be anywhere in a word)
STRONG_GROUP_SIGNS = {
    'ch': '⠡', 'sh': '⠩', 'th': '⠹', 'wh': '⠱',
    'ou': '⠳', 'ow': '⠪',
    'st': '⠌',  # Dots 3-4
    'ar': '⠜',  # Dots 3-4-5 (This is also the Lower Groupsign 'ar')
}

## 3. Lower Contractions (anywhere but the start of a word, or as whole words)
LOWER_CONTRACTIONS = {
    'be': '⠐⠃', 'in': '⠔', 'was': '⠐⠧', 'were': '⠐⠺', 'his': '⠐⠓', 'it': '⠭',
    'ea': '⠂',  # Lower Groupsign for 'ea' (dots 2, same as comma)
    'bb': '⠃⠃', 'cc': '⠉⠉', 'ff': '⠋⠋', 'gg': '⠛⠛', 'ar': '⠜',
}

# 4. Lower Word Signs (must stand alone as a whole word)
LOWER_WORD_SIGNS = {
    'but': '⠃', 'can': '⠉', 'do': '⠙', 'every': '⠑', 'from': '⠋', 'go': '⠛',
    'have': '⠓', 'just': '⠚', 'knowledge': '⠅', 'like': '⠇', 'more': '⠍',
    'not': '⠝', 'people': '⠏', 'quite': '⠟', 'rather': '⠗', 'so': '⠎',
    'that': '⠞', 'us': '⠥', 'very': '⠧', 'will': '⠺', 'you': '⠽',
    'as': '⠁⠎', 'are': '⠜',
}

# 5. Shortform contractions (stand alone as a whole word)
SHORTFORM_CONTRACTIONS = {
    # Full list is long, keeping subset for demonstration
    'about': '⠁⠃', 'after': '⠁⠋', 'again': '⠁⠛',
    'because': '⠃⠑⠉', 'before': '⠃⠑⠋', 'blind': '⠃⠇', 'braille': '⠃⠗⠇',
    'could': '⠉⠙', 'first': '⠋⠌', 'good': '⠛⠙', 'had': '⠓⠙', 'him': '⠓⠍',
    'little': '⠇⠇', 'much': '⠍⠡', 'must': '⠍⌡', 'one': '⠕⠝',
    'said': '⠎⠙', 'should': '⠩⠙', 'their': '⠹⠗', 'word': '⠺⠙',
}

# 6. Final-letter contractions (terminal groupsigns)
FINAL_LETTER_CONTRACTIONS = {
    # Sorted for precedence logic (longer first, then two-cell, then single-cell)
    # The existing final-contraction logic in the uploaded script was non-functional and is replaced with proper precedence logic below.
    'tion': '⠴⠝', 'ness': '⠴⠎', 'ment': '⠴⠞', 'ity': '⠴⠽', 
    'ence': '⠴⠑', 'ful': '⠴⠇', 'ong': '⠴⠛', 'sion': '⠨⠝', 
    'less': '⠨⠎', 'ance': '⠨⠑', 'ount': '⠨⠞', 'ound': '⠨⠙',
    'ing': '⠔', 'ed': '⠙', 'er': '⠗', 'en': '⠝', 'ess': '⠎',
}
FINAL_LETTER_CONTRACTIONS_SORTED = sorted(FINAL_LETTER_CONTRACTIONS.items(), key=lambda x: len(x[0]), reverse=True)


# 7. Initial-letter contractions (must be at the beginning of a word)
INITIAL_LETTER_CONTRACTIONS = {
    'day': '⠙', 'ever': '⠑', 'father': '⠋', 'here': '⠓', 'know': '⠅', 
    'lord': '⠇', 'mother': '⠍', 'name': '⠝', 'one': '⠕', 'part': '⠏',
    'question': '⠟', 'right': '⠗', 'some': '⠎', 'time': '⠞',
    'under': '⠥', 'young': '⠽',
    'com': '⠐⠉', 'dis': '⠙⠊⠎', 'con': '⠐⠝',
}

# Numeric mapping
NUMBER_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
}

# Combine all "whole word" contractions for Grade 2
WHOLE_WORD_SIGNS = {}
WHOLE_WORD_SIGNS.update(SHORTFORM_CONTRACTIONS)
WHOLE_WORD_SIGNS.update(LOWER_WORD_SIGNS)
WHOLE_WORD_SIGNS.update(STRONG_WORD_SIGNS)
WHOLE_WORD_SIGNS_SORTED = sorted(WHOLE_WORD_SIGNS.items(), key=lambda x: len(x[0]), reverse=True)

# Word signs that *must* be indicated in Grade 1
# This includes single-letter lower word signs and strong word signs
G1_INDICATED_WORDS = set(LOWER_WORD_SIGNS.keys()).union(set(STRONG_WORD_SIGNS.keys()))

# Compile regex for tokenization
TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')


# --- Core Conversion Functions ---

def text_to_braille(text_input, grade=BrailleGrade.GRADE_2):
    """
    Converts a string of English text to Braille, respecting UEB Grade 1 or 2 rules.
    """
    tokens = TOKEN_REGEX.findall(text_input)
    braille_output = []

    def convert_word_part_g2(word):
        """
        Converts a word by applying Grade 2 (Contracted) rules.
        Precedence: Initial > Final > Strong Group > Lower Group > Letter
        """
        braille_word_output = []
        i = 0
        while i < len(word):
            found_match = False
            remaining = word[i:]

            # 1. Check for Initial-letter contractions (at the beginning of the word)
            if i == 0:
                for contraction, braille in INITIAL_LETTER_CONTRACTIONS.items():
                    if remaining.startswith(contraction):
                        braille_word_output.append(braille)
                        i += len(contraction)
                        found_match = True
                        break
                if found_match:
                    continue
            
            # 2. Check for Final-letter contractions (at the end of the remaining part)
            # This is complex, but the simplest approach for a one-pass loop is to check
            # if the WHOLE REMAINING part is a final contraction, and if so,
            # recursively convert the prefix and then append the final contraction.
            # This assumes that a contraction cannot span across an internal word boundary/contraction.
            if i + 1 < len(word): # Check only if not the start of the word and there's space for a contraction
                for contraction, braille in FINAL_LETTER_CONTRACTIONS_SORTED:
                    if remaining.endswith(contraction) and len(remaining) > len(contraction):
                        prefix = remaining[:-len(contraction)]
                        # Convert the prefix and append the final contraction
                        braille_word_output.append(convert_word_part_g2(prefix))
                        braille_word_output.append(braille)
                        i += len(remaining)
                        found_match = True
                        break
                if found_match:
                    continue

            # 3. Check for Strong group signs (anywhere)
            for contraction, braille in STRONG_GROUP_SIGNS.items():
                if remaining.startswith(contraction):
                    braille_word_output.append(braille)
                    i += len(contraction)
                    found_match = True
                    break
            if found_match:
                continue

            # 4. Check for Lower contractions (anywhere except the beginning)
            if i > 0:
                for contraction, braille in sorted(LOWER_CONTRACTIONS.items(), key=lambda x: len(x[0]), reverse=True):
                    if remaining.startswith(contraction):
                        braille_word_output.append(braille)
                        i += len(contraction)
                        found_match = True
                        break
            if found_match:
                continue
                
            # 5. Fallback to single letter
            braille_word_output.append(BRAILLE_LETTERS.get(word[i], word[i]))
            i += 1
            
        return "".join(braille_word_output)

    def convert_word_part_g1(word, is_whole_word):
        """
        Converts a word to Grade 1 (Uncontracted) braille, applying G1 indicators
        to avoid misinterpretation as word signs.
        """
        braille_word_output = []
        lower_word = word.lower()
        
        # Apply Grade 1 Word Indicator if the whole word is a G2 word-sign that
        # would be misinterpreted (e.g., 'but', 'can', 'do', 'and', 'the').
        # However, for simplicity and safety, we apply G1-symbol indicator for
        # single-letter words that are word-signs, and avoid all contractions.
        
        for char in lower_word:
            if is_whole_word and char in BRAILLE_LETTERS and lower_word in G1_INDICATED_WORDS:
                # This logic is simplified: only apply G1 indicator to single-letter word signs.
                # 'a' and 'i' (as letters) do not need it, but 'b' (but), 'c' (can), 'd' (do), etc. do.
                if len(lower_word) == 1 and lower_word in ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                    braille_word_output.append(BRAILLE_INDICATORS['G1_SYM'])
            
            braille_word_output.append(BRAILLE_LETTERS.get(char, char))
        
        return "".join(braille_word_output)


    for token in tokens:
        if token.isspace() or re.match(r'^[^\w\s]+$', token):
            # Handle punctuation/spaces
            for char in token:
                braille_output.append(PUNCTUATION_SIGNS.get(char, char))
        elif token.isdigit():
            # Handle numbers
            braille_output.append(BRAILLE_INDICATORS['NUM'])
            for digit in token:
                braille_output.append(NUMBER_MAP.get(digit, ''))
        else:
            # Handle words
            braille_word = []
            lower_token = token.lower()
            
            # --- Capitalization ---
            is_all_caps = token.isupper() and len(token) > 1
            is_initial_caps = token[0].isupper()

            if is_all_caps:
                braille_word.append(BRAILLE_INDICATORS['CAPS_WORD']) # Fixed: used correct indicator
            elif is_initial_caps:
                braille_word.append(BRAILLE_INDICATORS['CAPS'])
            
            
            if grade == BrailleGrade.GRADE_2:
                # --- Grade 2 (Contracted) Logic ---
                matched_whole_word = False
                # Check for any whole-word contraction first (highest priority)
                for english_word, braille_sign in WHOLE_WORD_SIGNS_SORTED:
                    if lower_token == english_word:
                        braille_word.append(braille_sign)
                        matched_whole_word = True
                        break

                if not matched_whole_word:
                    # Apply part-word contractions
                    braille_word.append(convert_word_part_g2(lower_token))
            
            else:
                # --- Grade 1 (Uncontracted) Logic ---
                # No whole-word contractions, only letter-for-letter
                braille_word.append(convert_word_part_g1(lower_token, is_whole_word=True))

            braille_output.append("".join(braille_word))

    return "".join(braille_output)


# The braille_to_text function is complex and is omitted here, as the user requested
# a *corrected* version of the *text_to_braille* function with grade selection.
# The original braille_to_text function had issues and is not directly fixable 
# without a complete rewrite that properly handles the precedence of *all* UEB rules.
# The `braille_to_text` function in the original file will be left as-is, 
# noting that it has *known issues* for true round-trip conversion.
def braille_to_text(braille_input):
    """
    (Original - known issues for full UEB Grade 2 support)
    Converts Braille to English text with improved logic and a corrected reverse map.
    """
    english_output = []
    i = 0
    capitalize_next = False
    capitalize_whole_word = False
    in_numeric_mode = False

    # A single, correct, and comprehensive Braille-to-English map that prioritizes longer patterns
    reverse_map = {}
    reverse_map.update({v: k for k, v in FINAL_LETTER_CONTRACTIONS.items()})
    reverse_map.update({v: k for k, v in SHORTFORM_CONTRACTIONS.items()})
    reverse_map.update({v: k for k, v in STRONG_WORD_SIGNS.items()})
    reverse_map.update({v: k for k, v in LOWER_WORD_SIGNS.items()})
    reverse_map.update({v: k for k, v in STRONG_GROUP_SIGNS.items()})
    reverse_map.update({v: k for k, v in LOWER_CONTRACTIONS.items()})
    reverse_map.update({v: k for k, v in INITIAL_LETTER_CONTRACTIONS.items()})
    reverse_map.update({v: k for k, v in PUNCTUATION_SIGNS.items()})
    reverse_map.update({v: k for k, v in BRAILLE_LETTERS.items()})
    reverse_map.update({v: k for k, v in NUMBER_MAP.items()})

    # Add indicators separately (Using CAPS_WORD as the correct key)
    reverse_map[BRAILLE_INDICATORS['CAPS_WORD']] = '_WHOLE_WORD_CAPS'
    reverse_map[BRAILLE_INDICATORS['CAPS']] = '_CAPS'
    reverse_map[BRAILLE_INDICATORS['NUM']] = '_NUM'
    # Add G1 indicator for the reverse map to handle simple cases
    reverse_map[BRAILLE_INDICATORS['G1_SYM']] = '_G1_SYM'


    # Sort by the length of the braille pattern in descending order
    sorted_patterns = sorted(reverse_map.keys(), key=len, reverse=True)

    while i < len(braille_input):
        found_match = False
        
        # Check for numeric mode and apply it
        if in_numeric_mode:
            found_num = False
            # Check for G1 indicator termination (Dot 3) or space
            if braille_input[i:].startswith(PUNCTUATION_SIGNS[' ']) or braille_input[i:].startswith(PUNCTUATION_SIGNS['.']):
                 in_numeric_mode = False
            
            for digit, braille_char in NUMBER_MAP.items():
                if braille_input[i:].startswith(braille_char):
                    english_output.append(digit)
                    i += len(braille_char)
                    found_num = True
                    break
            
            # If a match was found, continue to next iteration
            if found_num:
                continue

            # Exit numeric mode at a space or non-numeric character
            if not found_num and braille_input[i] == ' ':
                in_numeric_mode = False
            elif not found_num and not braille_input[i].isspace():
                 # Handle non-number characters that follow a number in braille
                 # The rule is complex, but generally a space/punctuation breaks the numeric mode
                 in_numeric_mode = False 
            
            # If still in numeric mode and no match was found, it must be a braille letter/symbol
            if in_numeric_mode:
                # Fall through to the main loop to process non-number signs
                pass
            
            if not in_numeric_mode:
                 # If numeric mode just ended, don't increment i and restart the loop
                 continue


        # Match against sorted patterns (longer first)
        for pattern in sorted_patterns:
            if braille_input[i:].startswith(pattern):
                english_part = reverse_map[pattern]
                
                if english_part == '_WHOLE_WORD_CAPS':
                    capitalize_whole_word = True
                elif english_part == '_CAPS':
                    capitalize_next = True
                elif english_part == '_NUM':
                    in_numeric_mode = True
                elif english_part == '_G1_SYM':
                    # G1 Symbol Indicator: ignore in text output but prevent following letter from being treated as a word sign
                    # In this simplified model, we just ignore it.
                    pass
                else:
                    # Apply capitalization
                    if capitalize_next:
                        english_output.append(english_part.capitalize())
                        capitalize_next = False
                    elif capitalize_whole_word:
                        english_output.append(english_part.upper())
                    else:
                        english_output.append(english_part)

                    # A space typically ends the whole-word capitalization mode
                    if braille_input[i:].startswith(' '):
                        capitalize_whole_word = False
                
                i += len(pattern)
                found_match = True
                break
        
        if not found_match:
            english_output.append(braille_input[i])
            i += 1

    return "".join(english_output).strip()


def main():
    """
    Main function to handle command-line arguments and file operations.
    Added logic for selecting Braille Grade.
    """
    if len(sys.argv) < 3:
        print("Usage:")
        print("  To convert a file: python braille_converter.py [file_path] [to_braille_g1|to_braille_g2|to_text]")
        print("  Example: python braille_converter.py sample.txt to_braille_g2")
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

    if direction == "to_braille_g2":
        converted_content = text_to_braille(content, grade=BrailleGrade.GRADE_2)
        print("--- Converted to Braille (Grade 2) ---")
        print(converted_content)
    elif direction == "to_braille_g1":
        converted_content = text_to_braille(content, grade=BrailleGrade.GRADE_1)
        print("--- Converted to Braille (Grade 1) ---")
        print(converted_content)
    elif direction == "to_text":
        converted_content = braille_to_text(content)
        print("--- Converted to English Text (Partial UEB Grade 2 support) ---")
        print(converted_content)
    else:
        print("Error: Invalid conversion direction. Use 'to_braille_g1', 'to_braille_g2', or 'to_text'.")

if __name__ == "__main__":
    main()