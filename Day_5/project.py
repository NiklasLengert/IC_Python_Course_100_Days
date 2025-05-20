
# Password Generator
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like your password to have?\n"))
nr_symbols = int(input("How many symbols would you like?\n"))
nr_numbers = int(input("How many number would you like?\n"))

#easy level
# final_password = ""
# for i in range(nr_letters):
#     random_letter = random.choice(letters)
#     final_password += random_letter
# for i in range(nr_symbols):
#     random_symbol = random.choice(symbols)
#     final_password += random_symbol
# for i in range(nr_numbers):
#     random_number = random.choice(numbers)
#     final_password += random_number
# print(final_password)

#hard level
final_password = []
final_password_shuffled = ""
for i in range(nr_letters):
    random_letter = random.choice(letters)
    final_password.append(random_letter)
for i in range(nr_symbols):
    random_symbol = random.choice(symbols)
    final_password.append(random_symbol)
for i in range(nr_numbers):
    random_number = random.choice(numbers)
    final_password.append(random_number)
random.shuffle(final_password)
for item in final_password:
    final_password_shuffled += item
print(f"Your password is: {final_password_shuffled}.")
