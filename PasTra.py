#!/usr/bin/env python3
# PassTra.py - BIP39 Passphrase Translator
# By nakam0t0

import os
import signal
import sys
import locale
import io
import unicodedata
import re  # Import regex module for binary validation

class PassphraseTranslator:
    """
    A class for translating words between different languages according to the BIP39 standard,
    or finding a word by its binary index.

    BIP39 defines standardized word lists of 2048 words per language that are used
    in cryptocurrency wallets for mnemonic seed generation. This translator maps
    words between these different language dictionaries based on their index position,
    and can also find a word given its 11-bit binary index.
    """
    
    def __init__(self):
        """Initialize the translator with empty dictionaries and language settings."""
        self.dictionaries = {}
        self.source_lang = None
        self.target_lang = None
        self.load_available_dictionaries()
    
    def load_available_dictionaries(self):
        """Scan current directory for dictionary files and load them."""
        for filename in os.listdir("."):
            if filename.endswith(".txt") and os.path.isfile(filename):
                lang = os.path.splitext(filename)[0]
                try:
                    words = self.load_dictionary(filename)
                    if len(words) == 2048:  # Valid BIP39 dictionary must have 2048 words
                        self.dictionaries[lang] = words
                        print(f"Loaded dictionary: {lang}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def load_dictionary(self, filename):
        """
        Load a dictionary file with BIP39 words.
        
        Args:
            filename (str): The filename of the dictionary
            
        Returns:
            list: List of words from the dictionary
        """
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    
    def show_instructions(self):
        """Display instructions for using the translator."""
        print("\nBIP39 Passphrase Translator - Instructions")
        print("----")
        print("- If source is a language: Type a word to translate it to the target language")
        print("- If source is 'binary': Type an 11-bit binary string (e.g., 01101001110) to find the word in the target language")
        print("- Press Enter (empty input) to change languages/mode")
        print("- Type 'h' to show these instructions")
        print("- Type 'x' to exit the program")
        print("- Press Ctrl+C to exit at any time")
    
    def set_languages(self):
        """Prompt user to select source and target languages for translation by number."""
        print("\nAvailable languages:")

        print("\n0. binary")
        
        # Check if we have at least 2 dictionaries
        if len(self.dictionaries) < 2:
            print("Error: At least 2 dictionaries are required. Please add more dictionary files.")
            sys.exit(1)
        
        # Display languages with numbers
        langs = list(self.dictionaries.keys())
        for i, lang in enumerate(langs, 1):
            print(f"{i}. {lang}")
        
        # Select source language
        while True:
            source_input = input("\nEnter source language number: ").strip()
            try:
                source_idx = int(source_input) - 1
                if source_idx == -1:
                    self.source_lang = "binary"
                    break
                elif 0 <= source_idx < len(langs):
                    self.source_lang = langs[source_idx]
                    break
                else:
                    print(f"Invalid selection. Please enter a number between 0 and {len(langs)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Select target language
        while True:
            target_input = input("Enter target language number: ").strip()
            try:
                target_idx = int(target_input) - 1
                if 0 <= target_idx < len(langs):
                    self.target_lang = langs[target_idx]
                    if self.target_lang == self.source_lang:
                        print("Source and target languages must be different.")
                        continue
                    break
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(langs)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\nTranslating from {self.source_lang} to {self.target_lang}")
    
    def normalize_word(self, word):
        """
        Normalize a word for consistent comparison (lowercase and proper Unicode normalization).

        Args:
            word (str): The word to normalize

        Returns:
            str: Normalized word
        """
        if not word:
            return ""
        return unicodedata.normalize('NFKD', word.lower())
    
    def translate(self, word):
        """
        Translate a word from source language to target language, or find a word by binary index.
        Supports exact matches and prefix matching for words with 4 or more characters.

        Args:
            word (str): The word to translate or binary index to look up

        Returns:
            tuple: (source_word, target_word, index, binary) or (None, error_msg, None, None) if error
        """
        if not self.source_lang or not self.target_lang:
            return None, "Please set source and target languages first.", None, None

        # Handle binary input mode
        if self.source_lang == "binary":
            # Validate binary input format
            if not re.match(r'^[01]{11}$', word):
                return None, "Invalid binary input. Please enter exactly 11 bits (0s and 1s).", None, None

            try:
                # Convert binary to index (0-based)
                index = int(word, 2)
                if index >= 2048:
                    return None, "Binary value out of range (must be less than 2048).", None, None

                target_word = self.dictionaries[self.target_lang][index]
                return word, target_word, index + 1, word
            except ValueError:
                return None, "Invalid binary value.", None, None
            except Exception as e:
                return None, f"Error processing binary input: {str(e)}", None, None

        # Handle language-to-language translation
        normalized_word = self.normalize_word(word)
        if not normalized_word:
            return None, "Please enter a word to translate.", None, None

        try:
            matches = []
            # First try exact match
            try:
                index = self.dictionaries[self.source_lang].index(word)
                matches.append((
                    self.dictionaries[self.source_lang][index],
                    self.dictionaries[self.target_lang][index],
                    index + 1,
                    format(index, '011b')
                ))
            except ValueError:
                # Try normalized exact match
                for i, dict_word in enumerate(self.dictionaries[self.source_lang]):
                    if self.normalize_word(dict_word) == normalized_word:
                        matches.append((
                            dict_word,
                            self.dictionaries[self.target_lang][i],
                            i + 1,
                            format(i, '011b')
                        ))

            # If no exact match and word length >= 4, try prefix matching
            if not matches and len(normalized_word) >= 4:
                for i, dict_word in enumerate(self.dictionaries[self.source_lang]):
                    if self.normalize_word(dict_word).startswith(normalized_word):
                        matches.append((
                            dict_word,
                            self.dictionaries[self.target_lang][i],
                            i + 1,
                            format(i, '011b')
                        ))

            if not matches:
                if len(normalized_word) < 4:
                    return None, "Word not found. For partial matching, enter at least 4 characters.", None, None
                return None, "No matching words found in source dictionary.", None, None

            # Return first match if only one found
            if len(matches) == 1:
                return matches[0]

            # For multiple matches, return formatted string with all matches
            result = "Multiple matches found:\n"
            for src, tgt, idx, bin_val in matches:
                result += f"{src} → {tgt} | #{idx} | {bin_val}\n"
            return None, result.rstrip(), None, None

        except Exception as e:
            return None, f"Error during translation: {str(e)}", None, None
    
    def run_interface(self):
        """Run the interactive translator interface."""
        print("\nBIP39 Passphrase Translator")
        print("---------------------------")
        
        # Handle Ctrl+C gracefully
        def signal_handler(sig, frame):
            print("\nExiting the translator. Goodbye!")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        if not self.dictionaries:
            print("No dictionaries found. Please ensure .txt files are in the current directory.")
            return
        
        self.show_instructions()
        self.set_languages()
        
        while True:
            prompt_char = f"{self.source_lang}→{self.target_lang}" if self.source_lang != 'binary' else f"bin→{self.target_lang}"
            user_input = input(f"\n[{prompt_char}] > ").strip()
            
            # Handle special commands
            if user_input == "":
                # Empty input (Enter key) - change dictionaries
                self.set_languages()
                continue
            elif user_input.lower() == "h":
                # Show help instructions
                self.show_instructions()
                continue
            elif user_input.lower() == "x":
                # Exit the program
                print("Exiting the translator. Goodbye!")
                sys.exit(0)
            
            # Process word translation or binary lookup
            source_repr, result, index, binary = self.translate(user_input)

            if source_repr is not None:  # Success case
                target_word = result
                print(f"{source_repr} → {target_word} | #{index} | {binary}")
            else:
                # Failure case: result contains the error message
                error_message = result
                print(f"Error: {error_message}")

def configure_utf8():
    """Configure the terminal to properly handle UTF-8 characters."""
    # Set locale to user's default
    try:
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass
    
    # Configure standard output for UTF-8
    if sys.platform == "win32":
        # Windows-specific configuration
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)  # Set console code page to UTF-8
        except:
            pass
    
    # Ensure stdout is using UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def main():
    """Main function to run the PassphraseTranslator."""
    configure_utf8()
    translator = PassphraseTranslator()
    translator.run_interface()

if __name__ == "__main__":
    main()