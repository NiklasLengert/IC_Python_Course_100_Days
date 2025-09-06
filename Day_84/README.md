# Day 84 - Tic Tac Toe Game

A text-based implementation of the classic Tic Tac Toe game in Python.

## Features

- **Two-player gameplay** with custom player names
- **Interactive board display** with clear position numbers
- **Input validation** for moves and menu choices
- **Win detection** for all possible winning combinations
- **Tie detection** when board is full
- **Play again option** without restarting the program
- **Game rules display** for new players
- **Clean console interface** with screen clearing

## How to Play

1. Run the program: `python main.py`
2. Choose "Play Game" from the main menu
3. Enter names for both players
4. Players take turns entering positions (1-9)
5. First player to get 3 in a row wins!

## Game Rules

- The game is played on a 3x3 grid
- Player 1 uses X, Player 2 uses O
- Players take turns placing their marks
- Use numbers 1-9 to choose positions:

```
1 | 2 | 3
--|---|--
4 | 5 | 6
--|---|--
7 | 8 | 9
```

- First to get 3 in a row (horizontal, vertical, or diagonal) wins
- If all spaces are filled with no winner, it's a tie

## Game Structure

### Classes
- **TicTacToe**: Main game class handling board state, moves, and win detection

### Key Methods
- `display_board()`: Shows current game state
- `make_move(position)`: Places a mark on the board
- `check_winner()`: Checks for win conditions or ties
- `switch_player()`: Alternates between X and O

### Functions
- `get_player_names()`: Collects player names at start
- `get_valid_move()`: Handles input validation for moves
- `play_game()`: Main game loop
- `show_rules()`: Displays game instructions
- `main_menu()`: Program entry point with menu system

## Technical Features

- **Cross-platform screen clearing** (Windows/Unix)
- **Input validation** with error handling
- **Object-oriented design** with clean separation
- **Game state management** for multiple rounds
- **User-friendly interface** with clear prompts

## Learning Concepts

- Object-oriented programming with classes
- List manipulation and indexing
- Game state management
- Input validation and error handling
- Control flow with loops and conditionals
- Cross-platform compatibility
- User interface design in console applications

## Example Gameplay

```
==============================
       TIC TAC TOE
==============================

   |   |   
 X |   | O 
___|___|___
   |   |   
   | X |   
___|___|___
   |   |   
   |   |   
   |   |   

Player 1's turn (X)
```

## Files

- `main.py` - Complete Tic Tac Toe game implementation
- `README.md` - This documentation file
