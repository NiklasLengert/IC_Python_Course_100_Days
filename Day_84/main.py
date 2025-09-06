import os

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 30)
        print("       TIC TAC TOE")
        print("=" * 30)
        print()
        print("   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   ")
        print()
        
    def display_positions(self):
        print("Position numbers:")
        print("   |   |   ")
        print(" 1 | 2 | 3 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 4 | 5 | 6 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 7 | 8 | 9 ")
        print("   |   |   ")
        print()

    def make_move(self, position):
        if self.board[position - 1] == ' ':
            self.board[position - 1] = self.current_player
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' '):
                self.winner = self.board[combo[0]]
                self.game_over = True
                return True
        
        if ' ' not in self.board:
            self.game_over = True
            return True
        
        return False

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

def get_player_names():
    print("=" * 30)
    print("       PLAYER SETUP")
    print("=" * 30)
    print()
    player1 = input("Enter name for Player 1 (X): ").strip()
    if not player1:
        player1 = "Player 1"
    
    player2 = input("Enter name for Player 2 (O): ").strip()
    if not player2:
        player2 = "Player 2"
    
    return player1, player2

def get_valid_move():
    while True:
        try:
            move = input("Enter position (1-9): ").strip()
            if move == '':
                print("Please enter a position!")
                continue
            
            position = int(move)
            if 1 <= position <= 9:
                return position
            else:
                print("Please enter a number between 1 and 9!")
        except ValueError:
            print("Please enter a valid number!")

def play_game():
    game = TicTacToe()
    player1, player2 = get_player_names()
    
    players = {'X': player1, 'O': player2}
    
    while True:
        game.display_board()
        
        if game.game_over:
            if game.winner:
                print(f"🎉 {players[game.winner]} ({game.winner}) wins!")
            else:
                print("🤝 It's a tie!")
            
            print()
            play_again = input("Do you want to play again? (y/n): ").strip().lower()
            
            if play_again == 'y' or play_again == 'yes':
                game.reset_game()
                continue
            else:
                print("Thanks for playing!")
                break
        
        current_player_name = players[game.current_player]
        print(f"{current_player_name}'s turn ({game.current_player})")
        
        game.display_positions()
        
        position = get_valid_move()
        
        if game.make_move(position):
            if game.check_winner():
                game.display_board()
                if game.winner:
                    print(f"🎉 {players[game.winner]} ({game.winner}) wins!")
                else:
                    print("🤝 It's a tie!")
            else:
                game.switch_player()
        else:
            print("That position is already taken! Try again.")
            input("Press Enter to continue...")

def show_rules():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 40)
    print("           TIC TAC TOE RULES")
    print("=" * 40)
    print()
    print("1. The game is played on a 3x3 grid")
    print("2. Player 1 is X, Player 2 is O")
    print("3. Players take turns placing their marks")
    print("4. Use numbers 1-9 to choose position:")
    print()
    print("   1 | 2 | 3")
    print("   --|---|--")
    print("   4 | 5 | 6") 
    print("   --|---|--")
    print("   7 | 8 | 9")
    print()
    print("5. First to get 3 in a row wins!")
    print("6. Rows, columns, or diagonals count")
    print("7. If all spaces are filled, it's a tie")
    print()
    input("Press Enter to continue...")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 30)
        print("       TIC TAC TOE")
        print("=" * 30)
        print()
        print("1. Play Game")
        print("2. View Rules")
        print("3. Exit")
        print()
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            play_game()
        elif choice == '2':
            show_rules()
        elif choice == '3':
            print("Thanks for playing Tic Tac Toe!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
