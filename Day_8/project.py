
# Ceasar Cipher

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

life_cicle = True

def caesar(original_text, shift_amount, direction):
    changed_text = ""
    for letter in original_text:
        if letter in alphabet:
            if direction == "encode":
                new_position = alphabet.index(letter) + shift_amount
            elif direction == "decode":
                new_position = alphabet.index(letter) - shift_amount
            new_position %= len(alphabet)
            changed_text += alphabet[new_position]
        else:
            changed_text += letter
    print(f"Your text: {changed_text}")

while life_cicle == True:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    caesar(text, shift, direction)
    repeat = input("Type 'yes' if you want to go again or type 'no' to end the program.\n")
    if repeat == "no":
        life_cicle = False
        print("Ok goodbye :)")