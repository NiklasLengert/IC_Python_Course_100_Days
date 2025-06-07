
# Higher or Lower Game
# Planing:
# 1. Create a list of dictionaries with data about different follower counts of celebrities.
# 2. Randomly select two celebreties from the list.
# 3. Compare the follower counts of the two celebrities.
# 4. Ask the user to guess which celebrity has a higher follower count.
# 5. Provide feedback on the user's guess.
# 6. Keep track of the score and allow the user to play multiple rounds.

import random
from game_data import data
from art import logo, vs

def get_random_accounts():
    first_account = random.choice(data)
    second_account = random.choice(data)
    while first_account == second_account:
        second_account = random.choice(data)
    return first_account, second_account

def compare_followers(account_a, account_b):
    if account_a['follower_count'] > account_b['follower_count']:
        return 'a'
    else:
        return 'b'
    
def play_game():
    score = 0
    game_over = False
    account_a, account_b = get_random_accounts()

    print(logo)
    
    while not game_over:
        print(f"Compare A: {account_a['name']}, a {account_a['description']}, from {account_a['country']}.")
        print(vs)
        print(f"Against B: {account_b['name']}, a {account_b['description']}, from {account_b['country']}.")

        guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        correct_answer = compare_followers(account_a, account_b)

        if guess == correct_answer:
            score += 1
            print(f"You're right! Current score: {score}.")
            account_a = account_b
            account_b = get_random_accounts()[1]
        else:
            game_over = True
            print(f"Sorry, that's wrong. Final score: {score}.")

    print("Game Over!") 

if __name__ == "__main__":
    play_game()

