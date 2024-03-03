import re
import json

def parse_odds_line(line):
    match = re.match(r"\s*(.+?) with (.+?) for (.+)", line)
    team, bookmaker, odds = match.groups()
    return {"Team": team.strip(), "Bookmaker": bookmaker.strip(), "Odds": float(odds)}

def main():
    input_file = "output.txt"
    output_file = "parser_output.json" # Changed the extension to .json
    arbitrage_opportunities = []
    event_count = 0

    with open(input_file, "r") as infile:
        next(infile)  # Skip the first line
        lines = infile.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line:
            event_count += 1
            event = {}
            event["Event"] = event_count
            event["Bet_name"] = line
            i += 1
            total_implied_odds_line = lines[i]
            event["Total_implied_odds"] = float(re.findall(r"[-+]?\d*\.\d+|\d+", total_implied_odds_line)[0])
            i += 1

            odds_list = []
            while i < len(lines) and lines[i].strip() and "with" in lines[i]:
                odds_list.append(parse_odds_line(lines[i]))
                i += 1

            for idx, odds in enumerate(odds_list, start=1):
                event[f"odds_{idx}"] = odds

            arbitrage_opportunities.append(event)

    with open(output_file, "w") as outfile:
        json.dump(arbitrage_opportunities, outfile, indent=4) # Writing the data to a JSON file

if __name__ == "__main__":
    main()

