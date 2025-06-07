
# Coffee Machine Project

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "coffee": 24,
            "milk": 150,
        },
        "cost": 2.5
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "coffee": 24,
            "milk": 100,
        },
        "cost": 3.0
    }  
}

profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

is_on = True
while is_on:
    user_choice = input("What would you like? (espresso/latte/cappuccino): ").lower()
    if user_choice == "off":
        print("Turning off the coffee machine.")
        is_on = False
        break
    elif user_choice == "report":
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${profit:.2f}")
    elif user_choice in MENU:
        drink = MENU[user_choice]
        if all(resources[ingredient] >= amount for ingredient, amount in drink["ingredients"].items()):
            print(f"Please insert ${drink['cost']:.2f}")
            payment = float(input("Insert coins: "))
            if payment >= drink["cost"]:
                for ingredient, amount in drink["ingredients"].items():
                    resources[ingredient] -= amount
                change = payment - drink["cost"]
                profit += drink["cost"]
                if change > 0:
                    print(f"Here is ${change:.2f} in change.")
                print(f"Here is your {user_choice}. Enjoy!")
            else:
                print("Sorry, that's not enough money. Money refunded.")
        else:
            print("Sorry, not enough resources.")
    else:
        print("Invalid choice. Please try again.")
