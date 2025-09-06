MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', 
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': '/', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

def text_to_morse(text):
    morse_code = []
    text = text.upper()
    
    for char in text:
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        elif char == ' ':
            morse_code.append('/')
        else:
            morse_code.append('?')
    
    result = ' '.join(morse_code)
    return result

def morse_to_text(morse):
    reverse_dict = {}
    for key, value in MORSE_CODE_DICT.items():
        reverse_dict[value] = key
    
    morse_words = morse.split(' / ')
    decoded_words = []
    
    for word in morse_words:
        morse_chars = word.split(' ')
        decoded_chars = []
        
        for morse_char in morse_chars:
            if morse_char in reverse_dict:
                decoded_chars.append(reverse_dict[morse_char])
            elif morse_char == '':
                continue
            else:
                decoded_chars.append('?')
        
        decoded_word = ''.join(decoded_chars)
        decoded_words.append(decoded_word)
    
    result = ' '.join(decoded_words)
    return result

def display_menu():
    print("\n" + "="*50)
    print("        MORSE CODE CONVERTER")
    print("="*50)
    print("1. Convert Text to Morse Code")
    print("2. Convert Morse Code to Text")
    print("3. Show Morse Code Chart")
    print("4. Exit")
    print("="*50)

def show_morse_chart():
    print("\n" + "="*40)
    print("         MORSE CODE CHART")
    print("="*40)
    
    print("\nLETTERS:")
    letters = list(MORSE_CODE_DICT.items())[:26]
    for i in range(len(letters)):
        letter, morse = letters[i]
        print(f"{letter}: {morse:6}", end="  ")
        if (i + 1) % 4 == 0:
            print()
    
    print("\n\nNUMBERS:")
    numbers = list(MORSE_CODE_DICT.items())[26:36]
    for i in range(len(numbers)):
        num, morse = numbers[i]
        print(f"{num}: {morse:6}", end="  ")
        if (i + 1) % 5 == 0:
            print()
    
    print("\n\nSPECIAL CHARACTERS:")
    special_chars = list(MORSE_CODE_DICT.items())[36:]
    for char, morse in special_chars:
        print(f"{char}: {morse}")
    
    print("="*40)

def main():
    print("Welcome to the Morse Code Converter!")
    print("This program can convert text to Morse code and vice versa.")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-4): ")
            choice = choice.strip()
            
            if choice == '1':
                text_input = input("\nEnter text to convert to Morse code: ")
                text_input = text_input.strip()
                if text_input:
                    morse_result = text_to_morse(text_input)
                    print(f"\nOriginal Text: {text_input}")
                    print(f"Morse Code:    {morse_result}")
                else:
                    print("Please enter some text to convert!")
                    
            elif choice == '2':
                print("\nEnter Morse code to convert to text:")
                print("(Use spaces between letters, ' / ' between words)")
                print("Example: .... . .-.. .-.. --- / .-- --- .-. .-.. -..")
                morse_input = input("Morse Code: ")
                morse_input = morse_input.strip()
                
                if morse_input:
                    text_result = morse_to_text(morse_input)
                    print(f"\nMorse Code: {morse_input}")
                    print(f"Text:       {text_result}")
                else:
                    print("Please enter some Morse code to convert!")
                    
            elif choice == '3':
                show_morse_chart()
                
            elif choice == '4':
                print("\nThank you for using the Morse Code Converter!")
                print("Goodbye! 👋")
                break
                
            else:
                print("Invalid choice! Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
