## Usage Instructions

- When you start the program, it will show you available dictionaries and prompt you to select source and target languages
- Enter the number corresponding to each language when prompted
- Type a word from the source language to see its translation in the target language
- The program displays: source word, target word, word position number, and 11-bit binary representation

### Commands
- Press `Enter` (empty input) to change dictionaries
- Type `h` to show instructions
- Type `x` to exit the program
- Press `Ctrl+C` to exit at any time

## Example Usage

Below is an example of using the program:

```
 > python PasTra.py

 BIP39 Passphrase Translator
 Loaded dictionary: english Loaded dictionary: spanish

 BIP39 Passphrase Translator - Instructions
 Type a word to translate it from source to target language
 Press Enter (empty input) to change dictionaries
 Type 'h' to show these instructions
 Type 'x' to exit the program
 Press Ctrl+C to exit at any time
 Available languages:

 1.english
 2.spanish

 Enter source language number: 2
 Enter target language number: 1

 Translating from spanish to english

 > ábaco
 ábaco → abandon | #1 | 00000000000

 > abandonar
 abandonar → ability | #2 | 00000000001

 > abarca
 abarca → able | #3 | 00000000010

 >

 Available languages:

 1.english
 2.spanish

 Enter source language number: 1
 Enter target language number: 2

 Translating from english to spanish

 > abandon
 abandon → ábaco | #1 | 00000000000

 > h

 BIP39 Passphrase Translator - Instructions
 Type a word to translate it from source to target language
 Press Enter (empty input) to change dictionaries
 Type 'h' to show these instructions
 Type 'x' to exit the program
 Press Ctrl+C to exit at any time

 > x
 Exiting the translator. Goodbye!```
