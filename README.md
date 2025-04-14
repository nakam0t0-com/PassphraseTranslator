# PassphraseTranslator

A tool for translating BIP39 passphrases between languages and looking up words by their binary index.

## Features
- Translate BIP39 words between supported languages
- Look up words using their 11-bit binary index
- Support for partial word matching (minimum 4 characters)
- Display word position and binary representation
- Unicode normalization support
- Interactive command-line interface

## Requirements
- Python 3.6 or higher
- BIP39 word list files for desired languages (as .txt files in the same directory)

## Usage

1. Run the program using `python PasTra.py`
2. Select source and target languages from the available options
3. Enter words in the source language to see translations
4. Enter binary numbers (11 bits) to look up words by index
5. Use special commands for additional functions

### Commands
- Press `Enter` (empty input) to change dictionaries
- Type `h` to show instructions
- Type `x` to exit the program
- Type a binary number (11 bits) to look up words by index
- Press `Ctrl+C` to exit at any time

### Input Methods
- **Complete words**: Enter a complete word for exact translation
- **Partial words**: Enter at least 4 characters of a word for prefix matching
- **Binary mode**: Select "binary" as source language and enter 11-bit binary strings

## Example Usage

```
> python PasTra.py

BIP39 Passphrase Translator
Loaded dictionary: english Loaded dictionary: spanish

BIP39 Passphrase Translator - Instructions
Type a word to translate it from source to target language
Enter a binary number (11 bits) to look up words by index
Press Enter (empty input) to change dictionaries
Type 'h' to show these instructions
Type 'x' to exit the program
Press Ctrl+C to exit at any time

Available languages:
0. binary
1. english
2. spanish

Enter source language number: 2
Enter target language number: 1

Translating from spanish to english

> ábaco
ábaco → abandon | #1 | 00000000000

> 00000000001
Binary 00000000001 → ability/abandonar | #2

> abandonar
abandonar → ability | #2 | 00000000001

> 11111111111
Binary 11111111111 → zoo/zoológico | #2048

>

Available languages:
0. binary
1. english
2. spanish

Enter source language number: 0
Enter target language number: 1

[bin→english] > 00000000000 00000000000 → abandon | #1 | 00000000000

[bin→english] > 11111111111 11111111111 → zoo | #2048 | 11111111111

[bin→english] > x Exiting the translator. Goodbye!
```

## Word Matching Rules
- **Exact match**: The program first tries to find an exact match for the input word
- **Normalized match**: If no exact match is found, it tries to match using Unicode normalization
- **Prefix match**: For inputs of 4+ characters, it will find words that start with the input
- **Multiple matches**: If multiple words match the prefix, all matches will be displayed

## Binary Mode
- Select "binary" (option 0) as the source language
- Enter exactly 11 bits (0s and 1s) representing a word's index
- Valid range is from 00000000000 (0) to 11111111111 (2047)
- The corresponding word in the target language will be displayed

## Notes
- The program uses Unicode NFKD normalization for handling accented characters
- Binary indices are 11 bits long (0-2047) corresponding to BIP39 word positions
- Word lists must be in the standard BIP39 format with 2048 words each
- Dictionary files should be plain text (.txt) with one word per line
- Files are named according to the language (e.g., english.txt, spanish.txt)