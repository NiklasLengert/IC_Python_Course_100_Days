#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp
import os

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "Input/Letters/starting_letter.txt")) as letter_file:
    letter_content = letter_file.read()
with open(os.path.join(base_dir, "Input/Names/invited_names.txt")) as names_file:
    names = names_file.readlines()
for name in names:
    name = name.strip()
    letter = letter_content.replace("[name]", name)
    with open(os.path.join(base_dir, f"Output/ReadyToSend/letter_for_{name}.txt"), "w") as output_file:
        output_file.write(letter)