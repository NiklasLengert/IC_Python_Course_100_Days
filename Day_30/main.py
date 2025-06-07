import os

# FileNotFoundError
# file_path = os.path.join(os.path.dirname(__file__), "input.txt")
# with open(file_path) as file:
#     file.read()

# KeyError
# my_dict = {"name": "Alice", "age": 30}
# value = my_dict["helloKey"]

# IndexError
# my_list = [1, 2, 3]
# value = my_list[5]

# TypeError
# text = "Hello"
# print(text + 5)

# file_path = os.path.join(os.path.dirname(__file__), "input.txt")
# try:
#     file = open(file_path)
#     a_dict = {"name": "Alice", "age": 30}
#     print(a_dict["helloKey"])
# except FileNotFoundError:
#     file = open("input.txt", "w")
#     file.write("Hello, World!")
# except KeyError as error_message:
#     print(f"KeyError: {error_message}")
# else:
#     content = file.read()
#     print(content)
# finally:
#     file.close()
#     print("File closed.")
#     raise TypeError("This is a TypeError example.")


# height = float(input("Enter your height in meters: "))
# weight = int(input("Enter your weight in kilograms: "))

# if height <= 0 or weight <= 0:
#     raise ValueError("Height and weight must be positive numbers.")
# if height > 3 or weight > 500:
#     raise ValueError("Height and weight are unrealistic values.")
# bmi = weight / (height ** 2)
# print(f"Your BMI is: {bmi:.2f}")