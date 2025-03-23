#!/usr/bin/env python3
# PassTra.py - BIP39 Passphrase Translator
# By nakam0t0

import os
import signal
import sys
import locale
import io
import unicodedata

class PassphraseTranslator:
    """
    A class for translating words between different languages according to the BIP39 standard.
    
    BIP39 defines standardized word lists of 2048 words per language that are used
    in cryptocurrency wallets for mnemonic seed generation. This translator maps
    words between these different language dictionaries based on their index position.
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
        print("------------------------------------------")
        print("- Type a word to translate it from source to target language")
        print("- Press Enter (empty input) to change dictionaries")
        print("- Type 'h' to show these instructions")
        print("- Type 'x' to exit the program")
        print("- Press Ctrl+C to exit at any time")
    
    def set_languages(self):
        """Prompt user to select source and target languages for translation by number."""
        print("\nAvailable languages:")
        
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
                if 0 <= source_idx < len(langs):
                    self.source_lang = langs[source_idx]
                    break
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(langs)}.")
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
        # Convert to lowercase and apply Unicode normalization (NFC form)
        return unicodedata.normalize('NFC', word.lower())
    
    def translate(self, word):
        """
        Translate a word from source language to target language.
        
        Args:
            word (str): The word to translate from the source language
            
        Returns:
            tuple: (source_word, target_word, index, binary) or (None, None, None, None) if not found
        """
        if not self.source_lang or not self.target_lang:
            print("Please set source and target languages first.")
            return None, None, None, None
        
        normalized_word = self.normalize_word(word)
        
        try:
            # First try exact match
            index = self.dictionaries[self.source_lang].index(word)
            source_word = self.dictionaries[self.source_lang][index]
            target_word = self.dictionaries[self.target_lang][index]
            binary = format(index, '011b')
            return source_word, target_word, index + 1, binary
        except ValueError:
            # Try normalized match
            try:
                for i, dict_word in enumerate(self.dictionaries[self.source_lang]):
                    if self.normalize_word(dict_word) == normalized_word:
                        source_word = dict_word
                        target_word = self.dictionaries[self.target_lang][i]
                        binary = format(i, '011b')
                        return source_word, target_word, i + 1, binary
                return None, None, None, None
            except Exception:
                return None, None, None, None
    
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
            user_input = input("\n> ").strip()
            
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
            
            # Process word translation
            source_word, target_word, index, binary = self.translate(user_input)
            
            if source_word:
                print(f"{source_word} → {target_word} | #{index} | {binary}")
            else:
                print(f"Word '{user_input}' not found in {self.source_lang} dictionary.")

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