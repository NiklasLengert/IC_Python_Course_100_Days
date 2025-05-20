
# Number Guessing Game
import random

difficulties = {
    "easy": "20",
    "hard": "5"
}

user_guessed_correct = False
number_to_guess = random.randint(1, 100)
number_of_tries = 0
difficulty = input(f"Choose a difficulty. Type 'easy' or 'hard': ").lower()
print(f"You have {difficulties[difficulty]} attempts remaining to guess the number.")

while user_guessed_correct != True:
    user_guess = int(input("Make a guess: "))
    if(user_guess == number_to_guess):
        user_guessed_correct = True
        print("You have guessed the right number.")
    else:
        number_of_tries += 1 
        print(f"You guessed wrong number and you have {int(difficulties[difficulty]) - number_of_tries} tries left.")
        if int(difficulties[difficulty]) - number_of_tries == 0:
            print("You lost the game.")
            user_guessed_correct = True
        if(user_guess < number_to_guess):
            print("As a hint your number was too low.")
        else:
            print("As a hint your number was too high.")