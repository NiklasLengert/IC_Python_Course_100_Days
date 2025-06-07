
# File System

# # Manually closing a file after reading it
# file = open("Day_24/my_file.txt")
# contents = file.read()
# print(contents)
# file.close()

# # Using a context manager to automatically close the file
# with open("Day_24/my_file.txt", "w") as file:
#     file.write("New content added to the file.")

# with open("Day_24/my_file.txt", "r") as file:
#     contents = file.read()
#     print(contents)

with open("Day_24/my_file.txt", "a") as file:
    file.write("\nAppending this line to the file.")
with open("Day_24/my_file.txt", "r") as file:
    contents = file.read()
    print(contents)

    