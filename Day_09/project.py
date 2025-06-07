
# Secret Auction

def find_highest_bidder(bidding_dictionary):
    winner = ""
    highest_bid = 0
    for bidder in bidding_dictionary:
        bid_amount = int(bidding_dictionary[bidder])
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder
    print(f"The winner is {winner} with a bid of {highest_bid}$.")

auction_active = True
biding_dictionary = {}
while auction_active:
    print("Welcome to secret bidder.")
    name = input("Whats your name?")
    bid = input("How much do you want to bid?")

    biding_dictionary[name] = bid
    more_bidders = input("Are there more bidders yes|no?").lower()
    if(more_bidders == "no"):
        auction_active = False
        find_highest_bidder(biding_dictionary)
    elif(more_bidders == "yes"):
        print("\n" * 20)
