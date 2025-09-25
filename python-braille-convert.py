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
    # Basic Punctuation
    ' ': ' ', 
    '.': '⠲', # Period/Dot
    ',': '⠂', # Comma
    '!': '⠖', # Exclamation point
    '?': '⠦', # Question mark
    ':': '⠒', # Colon
    ';': '⠆', # Semicolon (Corrected from non-standard)
    '-': '⠤', # Hyphen
    
    # Quotation Marks (Directional - Double/Primary)
    '"': '⠦',  # Opening Double Quote (Corrected from non-directional)
    '”': '⠴',  # Closing Double Quote (Added for directional closure)

    # Apostrophe
    "'": '⠄', # Apostrophe/Closing Single Quote

    # Ellipsis (Multi-cell)
    '...': '⠲⠲⠲',
    
    # Dashes/Slashes (Multi-cell)
    '—': '⠠⠤',  # Em-dash/Long Dash (Added)
    '/': '⠸⠌',  # Forward Slash (Added)

    # Grouping Punctuation (Two-cell forms)
    '(': '⠐⠣', # Opening Parenthesis (Corrected from one-cell non-standard)
    ')': '⠐✜', # Closing Parenthesis (Corrected from one-cell non-standard)
    '[': '⠨⠣', # Opening Square Bracket (Added)
    ']': '⠨⠜', # Closing Square Bracket (Added)
}

# Key Braille indicators - EXPANDED UEB INDICATORS
BRAILLE_INDICATORS = {
    # Capitalization Indicators
    'CAPS': '⠠',                   # Capital Letter Indicator (Dot 6)
    'CAPS_WORD': '⠠⠠',              # Capital Word Indicator (Dot 6, Dot 6)
    'CAPS_PASSAGE': '⠠⠠⠠',         # Capital Passage Indicator (Dot 6, Dot 6, Dot 6)
    'CAPS_TERMINATOR': '⠠⠄',        # Capital Passage Terminator (Dot 6, Dot 3)

    # Grade 1 (Uncontracted) Indicators
    'G1_SYM': '⠰',                   # Grade 1 Symbol Indicator (Dots 5-6)
    'G1_WORD': '⠰⠰',                # Grade 1 Word Indicator (Dots 5-6, 5-6)
    'G1_PASSAGE': '⠰⠰⠰',             # Grade 1 Passage Indicator (Dots 5-6, 5-6, 5-6)
    'G1_TERMINATOR': '⠰⠄',          # Grade 1 Passage Terminator (Dots 5-6, 3)

    # Typeform Prefixes (Used with extent roots like ⠁, ⠂, ⠇, ⠄ for word/symbol/passage/terminator)
    'ITALIC_PREFIX': '⠨',            # Italic Typeform Prefix (Dots 4-6)
    'BOLD_PREFIX': '⠸',              # Bold Typeform Prefix (Dots 4-5-6)
    'UNDERLINE_PREFIX': '⠠⠨',       # Underline Typeform Prefix (Dots 6, 4-6)

    # Numeric, Subscript, Superscript Indicators
    'NUM': '⠼',                    # Numeric Indicator (Dots 3-4-5-6)
    'SUBSCRIPT_DOWN': '⠢',          # Subscript/Level Change Down (Dots 2-6)
    'SUPERSCRIPT_UP': '⠔',          # Superscript/Level Change Up (Dots 3-5)

    # Transcriber's Note Indicators (multi-cell symbols)
    'TRANS_NOTE_OPEN': '⠐⠨⠣',      # Transcriber's Note Open (Dots 5, 4-6, 1-2-6)
    'TRANS_NOTE_CLOSE': '⠐⠨⠜',     # Transcriber's Note Close (Dots 5, 4-6, 3-4-5)
}

# 1. Strong Word Signs (must stand alone as a whole word)
STRONG_WORD_SIGNS = {
    'and': '⠯', 'for': '⠫', 'of': '⠷', 'the': '⠮', 'with': '⠾',
    'child': '⠡', 'shall': '⠩', 'this': '⠹', 'which': '⠱', 'out': '⠳',
    'still': '⠌',
}

# 2. Strong Group Signs (can be anywhere in a word)
STRONG_GROUP_SIGNS = {
    # Strong Groupsigns (not covered by whole-word signs)
    'ch': '⠡', 'sh': '⠩', 'th': '⠹', 'wh': '⠱',
    'ou': '⠳', 'ow': '⠪',
    
    # Single-cell Strong Groupsigns
    'st': '⠌',  # Dots 3-4
    'ar': '⠜',  # Dots 3-4-5 (This is also the Lower Groupsign 'ar')
}

## 3. Lower Contractions (can be used as words or parts of words, but can't be at start of a word)
# Corrected: Removed eliminated UEB contractions ('by', 'to') and added missing UEB Lower Groupsign ('ea').
LOWER_CONTRACTIONS = {
    'be': '⠐⠃', 'in': '⠔', 'was': '⠐⠧', 'were': '⠐⠺', 'his': '⠐⠓', 'it': '⠭',
    'ea': '⠂',  # Added UEB Lower Groupsign for 'ea' (dots 2, same as comma)
    'bb': '⠃⠃', 'cc': '⠉⠉', 'ff': '⠋⠋', 'gg': '⠛⠛',
    # Eliminated UEB contractions 'by' and 'to' and incorrect multi-cell entries have been removed.
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
# Corrected: Added missing shortforms and corrected Braille notation based on UEB Appendix 1.
SHORTFORM_CONTRACTIONS = {
    'about': '⠁⠃', 'above': '⠁⠃⠧', 'according': '⠁⠉⠉', 
    'across': '⠁⠉⠗', # Added missing
    'after': '⠁⠋', 'again': '⠁⠛',
    'against': '⠁⠛⠌', # Corrected/Added
    'almost': '⠁⠇⠍', 'already': '⠁⠇⠗', 'also': '⠁⠇⠎', 'although': '⠁⠇⠹', # Corrected Braille
    'altogether': '⠁⠇⠞', 'always': '⠁⠇⠺', 
    'because': '⠃⠑⠉', 'before': '⠃⠑⠋', 'behind': '⠃⠓', 'below': '⠃⠇',
    'beneath': '⠃⠝', 'beside': '⠃⠎', 'between': '⠃⠞', 'beyond': '⠃⠽',
    'blind': '⠃⠇', # Added missing
    'braille': '⠃⠗⠇', 'character': '⠉⠓⠁', 
    'children': '⠡⠝', # Corrected Braille
    'conceive': '⠒⠉⠧', # Added missing
    'conceiving': '⠒⠉⠧⠛', # Added missing
    'could': '⠉⠙',
    'deceive': '⠙⠉⠧', # Added missing
    'deceiving': '⠙⠉⠧⠛', # Added missing
    'declare': '⠙⠉⠇', # Added missing
    'declaring': '⠙⠉⠇⠛', # Added missing
    'either': '⠑⠊', # Added missing
    'enough': '⠫', # Corrected Braille (Shortform for 'enough' is the same as the 'for' strong wordsign)
    'first': '⠋⠌', # Corrected Braille
    'friend': '⠋⠗', 'good': '⠛⠙', 
    'great': '⠛⠗⠞', # Corrected Braille
    'had': '⠓⠙',
    'her': '⠓⠻', # Added missing
    'herself': '⠓⠻⠋', # Corrected Braille
    'him': '⠓⠍', # Added missing
    'himself': '⠓⠍⠋', # Corrected Braille
    'immediate': '⠊⠍⠍', 
    'its': '⠭⠎', # Added missing
    'itself': '⠭⠋', # Added missing
    'letter': '⠇⠗', # Added missing
    'little': '⠇⠇', # Corrected Braille
    'made': '⠍⠙', 'many': '⠍⠁', 
    'much': '⠍⠡', # Added missing
    'must': '⠍⠌', # Corrected Braille
    'myself': '⠍⠽⠋', # Corrected Braille
    'necessary': '⠝⠑⠉', 'neither': '⠝⠑⠊', 
    'one': '⠕⠝', # Included for clarity as a whole word shortform
    'oneself': '⠐⠕⠋', # Added missing
    'ourselves': '⠳⠗⠧⠎', # Corrected Braille
    'paid': '⠏⠙', # Added missing
    'part': '⠏⠁', 
    'perceive': '⠏⠻⠉⠧', # Added missing
    'perceiving': '⠏⠻⠉⠧⠛', # Added missing
    'perhaps': '⠏⠻⠓', # Added missing
    'quick': '⠟⠅', 
    'receive': '⠗⠉⠧', # Added missing
    'receiving': '⠗⠉⠧⠛', # Added missing
    'rejoice': '⠗⠚⠉', # Added missing
    'rejoicing': '⠗⠚⠉⠛', # Added missing
    'right': '⠗⠣', 'said': '⠎⠙', 'some': '⠎⠍', 'spirit': '⠎⠏', 
    'should': '⠩⠙', # Added missing
    'such': '⠎⠉⠓', # Corrected Braille
    'their': '⠹⠗', 'these': '⠹⠎', 'themselves': '⠹⠑⠍⠧⠎', # Corrected Braille
    'through': '⠹⠗', 
    'thyself': '⠹⠽⠋', # Added missing
    'time': '⠞⠊', 'today': '⠞⠙', 'together': '⠞⠛', 'tomorrow': '⠞⠍', 'tonight': '⠞⠝',
    'under': '⠥⠝', 'upon': '⠥⠏', 'where': '⠱', 'which': '⠱', 'who': '⠱', 'whose': '⠱⠎',
    'word': '⠺⠙', 'work': '⠺⠅', 'world': '⠺⠇', 
    'would': '⠺⠙', # Corrected Braille
    'young': '⠽⠛',
    'your': '⠽⠗', 
    'yourself': '⠽⠗⠋', # Corrected Braille
    'yourselves': '⠽⠗⠧⠎', # Corrected Braille
}

# 6. Final-letter contractions (All 17 terminal groupsigns)
FINAL_LETTER_CONTRACTIONS = {
    # 5 Single-Cell Terminal Groupsigns
    'ing': '⠔',  # Dots 3-4-6 (G sign)
    'ed': '⠙',   # Dots 1-4-5 (D sign)
    'er': '⠗',   # Dots 1-2-3-5 (R sign)
    'en': '⠝',   # Dots 1-3-4-5 (N sign)
    'ess': '⠎',  # Dots 2-3-4 (S sign)

    # 12 Two-Cell Terminal Groupsigns (Dot 5-6 Prefix - ⠴)
    'tion': '⠴⠝', # Dots 5-6, 1-3-4-5
    'ness': '⠴⠎', # Dots 5-6, 2-3-4
    'ment': '⠴⠞', # Dots 5-6, 2-3-4-5
    'ity': '⠴⠽',  # Dots 5-6, 1-3-4-5-6
    'ence': '⠴⠑', # Dots 5-6, 1-5
    'ful': '⠴⠇',  # Dots 5-6, 1-2-3
    'ong': '⠴⠛',  # Dots 5-6, 1-2-4-5

    # 12 Two-Cell Terminal Groupsigns (Dot 4-6 Prefix - ⠨)
    'sion': '⠨⠝', # Dots 4-6, 1-3-4-5
    'less': '⠨⠎', # Dots 4-6, 2-3-4
    'ance': '⠨⠑', # Dots 4-6, 1-5
    'ount': '⠨⠞', # Dots 4-6, 2-3-4-5
    'ound': '⠨⠙', # Dots 4-6, 1-4-5
}

# 7. Initial-letter contractions (must be at the beginning of a word)
INITIAL_LETTER_CONTRACTIONS = {
    'day': '⠙', 'ever': '⠑', 'father': '⠋', 'here': '⠓', 'know': '⠅', # CORRECTED 'ever'
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

# Compile regex for tokenization
TOKEN_REGEX = re.compile(r'([A-Za-z]+|\d+|[^\w\s]|\s+)')

def text_to_braille(text_input):
    """
    Converts a string of English text to Braille using a precedence-based approach.
    """
    tokens = TOKEN_REGEX.findall(text_input)
    braille_output = []

    # Combine all "whole word" contractions into a single dictionary for easier lookup.
    # This ensures that shortforms and other word signs are checked first.
    WHOLE_WORD_SIGNS = {}
    WHOLE_WORD_SIGNS.update(SHORTFORM_CONTRACTIONS)
    WHOLE_WORD_SIGNS.update(LOWER_WORD_SIGNS)
    WHOLE_WORD_SIGNS.update(STRONG_WORD_SIGNS)
    # Also add contractions from other lists that can be used as whole words
    WHOLE_WORD_SIGNS.update({v: k for k, v in STRONG_GROUP_SIGNS.items()})
    WHOLE_WORD_SIGNS.update({v: k for k, v in LOWER_CONTRACTIONS.items()})
    WHOLE_WORD_SIGNS.update({v: k for k, v in FINAL_LETTER_CONTRACTIONS.items()})
    
    # Sort these for precedence (longer matches first)
    WHOLE_WORD_SIGNS_SORTED = sorted(WHOLE_WORD_SIGNS.items(), key=lambda x: len(x[0]), reverse=True)

    def convert_word_part(word):
        """
        Converts a word by applying the most specific contractions first, respecting placement rules.
        """
        braille_word_output = []
        i = 0
        while i < len(word):
            found_match = False
            remaining = word[i:]

            # 1. Check for Initial-letter contractions (at the beginning)
            if i == 0:
                for contraction, braille in INITIAL_LETTER_CONTRACTIONS.items():
                    if remaining.startswith(contraction):
                        braille_word_output.append(braille)
                        i += len(contraction)
                        found_match = True
                        break
                if found_match:
                    continue

            # 2. Check for Strong group signs (anywhere)
            for contraction, braille in STRONG_GROUP_SIGNS.items():
                if remaining.startswith(contraction):
                    braille_word_output.append(braille)
                    i += len(contraction)
                    found_match = True
                    break
            if found_match:
                continue

            # 3. Check for Final-letter contractions (at the end)
            # Prioritize longer final contractions like 'tion' before 'ing'
            final_sorted = sorted(FINAL_LETTER_CONTRACTIONS.items(), key=lambda x: len(x[0]), reverse=True)
            for contraction, braille in final_sorted:
                if remaining.endswith(contraction):
                    if len(remaining) == len(contraction):
                        braille_word_output.append(braille)
                        i += len(remaining)
                        found_match = True
                        break
                    else:
                        prefix = remaining[:-len(contraction)]
                        braille_word_output.append(convert_word_part(prefix))
                        braille_word_output.append(braille)
                        i += len(remaining)
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
            
            # Check for any whole-word contraction first
            matched_whole_word = False
            for english_word, braille_sign in WHOLE_WORD_SIGNS_SORTED:
                if lower_token == english_word:
                    braille_word.append(braille_sign)
                    matched_whole_word = True
                    break

            if not matched_whole_word:
                braille_word.append(convert_word_part(lower_token))

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

    # Add indicators separately
    reverse_map[BRAILLE_INDICATORS['WHOLE_WORD_CAPS']] = '_WHOLE_WORD_CAPS'
    reverse_map[BRAILLE_INDICATORS['CAPS']] = '_CAPS'
    reverse_map[BRAILLE_INDICATORS['NUM']] = '_NUM'

    # Sort by the length of the braille pattern in descending order
    sorted_patterns = sorted(reverse_map.keys(), key=len, reverse=True)

    while i < len(braille_input):
        found_match = False
        
        # Check for numeric mode and apply it
        if in_numeric_mode:
            found_num = False
            for digit, braille_char in NUMBER_MAP.items():
                if braille_input[i:].startswith(braille_char):
                    english_output.append(digit)
                    i += len(braille_char)
                    found_num = True
                    break
            
            # Exit numeric mode at a space or non-numeric character
            if not found_num or braille_input[i] == ' ':
                in_numeric_mode = False
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
