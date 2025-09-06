# Day 82 - Morse Code Converter

A text-based Python program that converts strings to Morse Code and vice versa.

## Features

- **Text to Morse Code**: Convert any text string to Morse code
- **Morse Code to Text**: Decode Morse code back to readable text  
- **Morse Code Chart**: Display the complete Morse code reference chart
- **User-friendly Menu**: Simple interactive menu system
- **Error Handling**: Handles invalid inputs gracefully

## Supported Characters

- **Letters**: A-Z (converted to uppercase)
- **Numbers**: 0-9
- **Special Characters**: Common punctuation marks (, . ? ' ! / ( ) & : ; = + - _ " $ @)
- **Spaces**: Converted to '/' in Morse code

## How to Use

1. Run the program: `python main.py`
2. Choose from the menu options:
   - **Option 1**: Enter text to convert to Morse code
   - **Option 2**: Enter Morse code to convert back to text
   - **Option 3**: View the complete Morse code chart
   - **Option 4**: Exit the program

## Morse Code Format

- **Letters/Numbers**: Separated by single spaces
- **Words**: Separated by ' / ' (space-slash-space)
- **Example**: "HELLO WORLD" becomes ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

## Example Usage

```
Enter text to convert to Morse code: Hello World 123
Original Text: Hello World 123
Morse Code:    .... . .-.. .-.. --- / .-- --- .-. .-.. -.. / .---- ..--- ...--
```

## Learning Concepts Demonstrated

- Dictionary mapping and lookups
- String manipulation and processing
- User input validation
- Menu-driven program structure
- Function organization and documentation
- Error handling with try-catch
- List comprehensions and string methods

## Files

- `main.py` - Main program file containing all functionality
- `README.md` - This documentation file
