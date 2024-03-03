import json

# Load the JSON file
with open('parser_output.json', 'r') as file:
    parser_output = json.load(file)

max_profits = []

for event in parser_output:
    start_amount = 1
    max_amount = 1000
    max_profit = 0
    
    best_current_amount = 0  # Track the current amount that produces the maximum profit
    best_bets = {"odds_1": 0, "odds_2": 0, "odds_3": 0}  # Amount to bet on each odd

    for current_amount in range(start_amount, max_amount + 1):
        odds_1_bet = int(current_amount / event["odds_1"]["Odds"])
        odds_2_bet = int(current_amount / event["odds_2"]["Odds"])
        odds_3_bet = int(current_amount / event["odds_3"]["Odds"]) if "odds_3" in event else 0

        total_profit = current_amount - sum([odds_1_bet, odds_2_bet, odds_3_bet])

        if total_profit > max_profit:
            max_profit = int(total_profit)
            best_current_amount = current_amount  # Update the best current amount
            best_bets["odds_1"] = odds_1_bet
            best_bets["odds_2"] = odds_2_bet
            best_bets["odds_3"] = odds_3_bet
    
    print(f"Event {event['Event']}: {event['Bet_name']}")
    print(f"Max Profit: {max_profit}")
    print(f"Total Amount for Max Profit: {best_current_amount}")
    for odd, bet in best_bets.items():
        if bet != 0:
            print(f"Amount to bet on {odd}: {bet}")
    print()

    # Append the maximum profit and event number to the list
    if max_profit > 1:
        max_profits.append((max_profit, event['Event']))

# Sort the maximum profits in descending order
max_profits.sort(reverse=True, key=lambda x: x[0])

print("Max Profits from High to Low:")
for profit, event_number in max_profits:
    print(f"Event {event_number}: Max Profit = {profit}")

# Summing the maximum profits from the max_profits list
total_max_profit = sum(profit for profit, _ in max_profits)
print(f"Total Max Profit: {total_max_profit}")
