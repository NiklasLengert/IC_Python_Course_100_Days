
# Rock Paper Scissors
import random

word_list = ["rock", "paper", "scissors"]
print("Welcome to rock paper scissors. You can type 0 for rock, 1 for paper and 2 for scissors.")
user_choice = int(input("Please choose your competitor.(Remember rock is 0, paper is 1 and scissors is 2) "))
computer_choice = random.randint(0, 2)
print(f"{user_choice} and {computer_choice}")
if(user_choice == computer_choice):
    print(f"Computer choose: {word_list[computer_choice]}. We got a draw.")
elif(user_choice == 0 and computer_choice == 1):
    print(f"Computer choose: {word_list[computer_choice]}. You lost.")
elif(user_choice == 0 and computer_choice == 2):
    print(f"Computer choose: {word_list[computer_choice]}. You won.")
elif(user_choice == 1 and computer_choice == 0):
    print(f"Computer choose: {word_list[computer_choice]}. You won.")
elif(user_choice == 1 and computer_choice == 2):
    print(f"Computer choose: {word_list[computer_choice]}. You lost.")
elif(user_choice == 2 and computer_choice == 0):
    print(f"Computer choose: {word_list[computer_choice]}. You lost.")
elif(user_choice == 2 and computer_choice == 1):
    print(f"Computer choose: {word_list[computer_choice]}. You won.")
    