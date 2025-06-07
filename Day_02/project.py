
# Tip Calculator

print("Welcome to the tip calculator!")
total_bill = float(input("What was the total bill?\n"))
tip_percentage = float(input("How much tip would you like to give?\n"))
amount_of_people = int(input("How many people want to split the bill?\n"))

amount_split = (total_bill + (total_bill * (tip_percentage / 100))) / amount_of_people
print(f"Each person should pay: ${amount_split}")