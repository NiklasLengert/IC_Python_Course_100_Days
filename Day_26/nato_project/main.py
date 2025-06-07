import os
nato_file_path = os.path.join(os.path.dirname(__file__), "nato_phonetic_alphabet.csv")

student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

#Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

import pandas

student_data_frame = pandas.DataFrame(student_dict)

#Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    #Access index and row
    #Access row.student or row.score
    pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}
nato_data = pandas.read_csv(nato_file_path)
nato_dict = {row.letter: row.code for (row, row) in nato_data.iterrows()}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
def generate_phonetic_code():
    word = input("Enter a word: ").upper()
    try:
        phonetic_code = [nato_dict[letter] for letter in word if letter in nato_dict]
        print(phonetic_code)
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic_code()
generate_phonetic_code()

