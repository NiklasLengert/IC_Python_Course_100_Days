
# Bugs

# from random import randint
# dice_images = [
#     "⚀",  # 1
#     "⚁",  # 2
#     "⚂",  # 3
#     "⚃",  # 4
#     "⚄",  # 5
#     "⚅"   # 6
# ]
# dice_num = randint(1, 6) # <-- Bug is here in the range
# print(dice_images[dice_num])


# year = int(input("Whats your year of birth?"))
# if 1980 < year < 1994: # <-- Bug since 1994 is never checked only above or below
#     print("You are a millennial")
# elif year > 1994:
#     print("Your are a Gen Z.")


# try:
#     age = int(input("How old are you?"))
# except ValueError:
#     print("You have typed in an invalid number.")
#     age = int(input("How old are you? "))
# if age > 18:
#     print(f"You can drive at age {age}.")


# word_per_page = 0
# pages = int(input("Number of pages: "))
# word_per_page = int(input("Number of words per page: "))
# total_words = pages * word_per_page
# print(total_words)


# import random 
# import maths

# def mutate(a_list):
#     b_list = []
#     new_item = 0
#     for item in a_list:
#         new_item = item * 2
#         new_item += random.randint(1, 3)
#         new_item = maths.add(new_item, item)
#         b_list.append(new_item)
#     print(b_list)

# mutate([1, 2, 3, 5, 8, 13])
