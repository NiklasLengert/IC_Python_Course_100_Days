# Treasure Island

print("Welcome to Treasure Island. Your mission is to find the treasure.")
first_direction = input("You stand at a crossroad. Do you want to go left or right?")
if first_direction == "left":
    second_direction = input("You continue your way until you reach a river. Do you swim or wait?")
    if second_direction == "wait":
        third_direction = input("You find a house with three doors. A red, blue and yellow one. Through which door do you go?")
        if third_direction == "yellow":
            print("You Win!")
        else:
            print("The door locked behind you and the room began to burn. Game Over")
    else:
        print("A shark attacked you. Game Over")
else:
    print("A wolf attacked you. Game Over")