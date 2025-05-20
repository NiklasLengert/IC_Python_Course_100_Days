
# Calculator

calculator_power = True
result_holder = 0

def addition(num1, num2):
    return num1 + num2

def subtraction(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def division(num1, num2):
    return num1 / num2

operations_dictionary = {}
operations_dictionary["+"] = addition
operations_dictionary["-"] = subtraction
operations_dictionary["*"] = multiply
operations_dictionary["/"] = division

def calculate(num1, num2, operation, operations_dict):
    if(operation == "+"):
        result_holder = operations_dict["+"](num1, num2)
        return result_holder
    elif(operation == "-"):
        result_holder = operations_dict["-"](num1, num2)
        return result_holder
    elif(operation == "*"):
        result_holder = operations_dict["*"](num1, num2)
        return result_holder
    elif(operation == "/"):
        result_holder = operations_dict["/"](num1, num2)
        return result_holder
    else:
        print("Upps something went wrong.")

first_num = float(input("Whats the first nubmer?: "))        

while calculator_power:
    operation = input("+ \n- \n* \n/ \nPick an operation by typing one of the symbols: ")
    second_num = float(input("Whats the second number? "))

    result = calculate(first_num, second_num, operation, operations_dictionary)
    
    user_choice = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation, or type 's' to stop the calculator: ")
    if user_choice == "s":
        calculator_power = False
    elif user_choice == "n":
        first_num = float(input("Whats the first nubmer?: ")) 
    elif user_choice == "y":
        first_num = result
