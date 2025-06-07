
# List Comprehensions
# List comprehensions provide a concise way to create lists.
# Example: Create a list of squares of numbers from 0 to 9

# numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# new_list = []
# for number in numbers:
#     new_list.append(number ** 2)
# print(new_list)
# # Using list comprehension 
# new_list = [number ** 2 for number in numbers]
# print(new_list)

# name = "Niklas"
# new_list = [letter for letter in name]
# print(new_list)

# double_numbers = [number * 2 for number in range(1, 11)]
# print(double_numbers)

# names = ["Niklas", "Max", "John", "Jane", "Alice"]
# long_names = [name.upper() for name in names if len(name) > 5]
# print(long_names)

# Dictionary Comprehensions
# Dictionary comprehensions allow you to create dictionaries in a similar way to list comprehensions.

# student_scores = {
#     "Niklas": 90,
#     "Max": 85,
#     "John": 78,
#     "Jane": 92,
#     "Alice": 88
# }

# student_scores = {student: random.randint(50, 100) for student in names}

# # Create a new dictionary with names as keys and scores as values
# student_scores = {name:score for (name, score) in student_scores.items() if score > 80}
# print(student_scores)

# student_dict = {
#     "student": ["Niklas", "Max", "John", "Jane", "Alice"],
#     "score": [90, 85, 78, 92, 88]
# }

# for (key, value) in student_dict.items():
#     print(f"{key}: {value}")

# import pandas as pd

# pd_student = pd.DataFrame(student_dict)
# print(pd_student)

# for (key, value) in pd_student.items():
#     print(value)

# for (index, row) in pd_student.iterrows():
#     print(row.student)
#     print(row.score)


