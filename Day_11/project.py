
# Black Jack

import random

game_state = True
game_state_dissicion = ""
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
hand_user = []
hand_computer = []
user_score = 0
computer_score = 0

def draw_card(card_list):
    card_one = random.choice(card_list)
    card_two = random.choice(card_list)
    return card_one, card_two

def add_cards_to_hands(card, hand):
    hand.append(card)

def calculate_score(hand):
    if sum(hand) == 21 and len(hand) == 2:
        return 0
    if 11 in hand and sum(hand) > 21:
        hand.remove(11)
        hand.append(1)
    return sum(hand)

def game_state_check(computer_score, user_score):
    if user_score == 0:
        print(f"Your final hand: {hand_user}, final score: 21")
        print(f"Computer's final hand: {hand_computer}, final score: {computer_score}")
        print("You win with a Blackjack! 😎")
        return False
    elif computer_score == 0:
        print(f"Your final hand: {hand_user}, final score: {user_score}")
        print(f"Computer's final hand: {hand_computer}, final score: 21")
        print("Computer wins with a Blackjack! 😞")
        return False
    
    if user_score > 21:
        print(f"Your final hand: {hand_user}, final score: {user_score}")
        print(f"Computer's final hand: {hand_computer}, final score: {computer_score}")
        print("You went over. You lose! 😭")
        return False
    elif computer_score > 21:
        print(f"Your final hand: {hand_user}, final score: {user_score}")
        print(f"Computer's final hand: {hand_computer}, final score: {computer_score}")
        print("Computer went over. You win! 🎉")
        return False
    
    print(f"Your cards: {hand_user}, current score: {user_score}")
    print(f"Computer's cards: {hand_computer}, current score: {computer_score}")
    return True


while game_state:
    game_state_dissicion = input("Do you want to play a round of black jack. If yes type 'y' or 'n' for no. ").lower()
    if game_state_dissicion == "no":
        break
    else:
        new_card01, new_card02 = draw_card(cards)
        if computer_score <= 16:
            add_cards_to_hands(new_card01, hand_computer)
            computer_score = calculate_score(hand_computer)
        want_draw = input(f"Do you want to draw another card (y/n). Your current score is {user_score} ").lower()
        if want_draw == "y":
            add_cards_to_hands(new_card02, hand_user)
            user_score = calculate_score(hand_user)
        if want_draw == "n":
            break
        game_state = game_state_check(computer_score, user_score)




