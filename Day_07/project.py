
# Today there is no practice only one project which is to code hangman
import random

word_list = ["aardvark", "baboon", "camel"]
random_word = random.choice(word_list)
random_word_as_list = []
random_word_hidden = []
end_signal = False
revealed_letters = 0
lifes = 6
for letter in random_word:
    random_word_as_list.append(letter)
    random_word_hidden.append("_")
print(random_word_as_list)

while end_signal is False:

    user_guess = input("Please guess a letter which you think is in the word. ").lower()

    if user_guess in random_word_as_list:
        print("Yes, that letter is in the word.")
        for i in range(len(random_word_as_list)):
            if random_word_as_list[i] == user_guess:
                random_word_hidden[i] = user_guess
                revealed_letters += 1
        print("Good guess")
        if revealed_letters == len(random_word_as_list):
            print("You have won!")
            end_signal = True
    else:
        lifes -= 1
        print(f"Sorry, that letter is not in the word. You have {lifes} tries left.")
    print(random_word_hidden)

