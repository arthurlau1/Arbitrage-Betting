import json

# Load the JSON file
with open('parser_output.json', 'r') as file:
    parser_output = json.load(file)

V = 1000

def calculate_arbitrage_two_outcomes(K1, K2, V):
    L = 1/K1 + 1/K2
    if L < 1:
        L2 = K1 / K2
        V1 = int(V / (1 + L2))
        V2 = int((L2 * V) / (1 + L2))
        return V1, V2
    else:
        return None, None

def calculate_arbitrage_three_outcomes(K1, K2, K3, V):
    L = 1/K1 + 1/K2 + 1/K3
    if L < 1:
        L2 = K1 / K2
        L3 = (1 + L2) / (K3 - 1)
        V1 = int(V / (1 + L2 + L3))
        V2 = int((L2 * V) / (1 + L2 + L3))
        V3 = int((L3 * V) / (1 + L2 + L3))
        return V1, V2, V3
    else:
        return None, None, None

def calculate_profit_two_outcomes(V, V1, K1, V2, K2):
    profit1 = V1 * K1 - V
    profit2 = V2 * K2 - V
    return int(max(profit1, profit2))

def calculate_profit_three_outcomes(V, V1, K1, V2, K2, V3, K3):
    profit1 = V1 * K1 - V
    profit2 = V2 * K2 - V
    profit3 = V3 * K3 - V
    return int(max(profit1, profit2, profit3))

# Calculate profits and store in the dictionary
for opportunity in parser_output:
    # Two odds arbitrage
    if "odds_3" not in opportunity:
        K1 = opportunity["odds_1"]["Odds"]
        K2 = opportunity["odds_2"]["Odds"]
        
        V1, V2 = calculate_arbitrage_two_outcomes(K1, K2, V)
        
        if V1:
            opportunity['profit'] = calculate_profit_two_outcomes(V, V1, K1, V2, K2)
            print(f"Event {opportunity['Event']}: {opportunity['Bet_name']}")
            print(f"Bet on {opportunity['odds_1']['Team']}: ${V1}")
            print(f"Bet on {opportunity['odds_2']['Team']}: ${V2}")
            print("*" * 50)
    # Three odds arbitrage
    else:
        K1 = opportunity["odds_1"]["Odds"]
        K2 = opportunity["odds_2"]["Odds"]
        K3 = opportunity["odds_3"]["Odds"]
        
        V1, V2, V3 = calculate_arbitrage_three_outcomes(K1, K2, K3, V)
        
        if V1:
            opportunity['profit'] = calculate_profit_three_outcomes(V, V1, K1, V2, K2, V3, K3)
            print(f"Event {opportunity['Event']}: {opportunity['Bet_name']}")
            print(f"Bet on {opportunity['odds_1']['Team']}: ${V1}")
            print(f"Bet on {opportunity['odds_2']['Team']}: ${V2}")
            print(f"Bet on {opportunity['odds_3']['Team']}: ${V3}")
            print("*" * 50)

# Sort the list by profit in descending order
sorted_opportunities = sorted(parser_output, key=lambda x: x['profit'], reverse=True)

# Display sorted opportunities
for opportunity in sorted_opportunities:
    print(f"Event {opportunity['Event']}: {opportunity['Bet_name']}")
    if 'profit' in opportunity:
        print(f"Max Expected Profit: ${opportunity['profit']}")
    else:
        print("No arbitrage opportunity.")
    print("-" * 50)
