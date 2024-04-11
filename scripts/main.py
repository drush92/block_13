import json
import random
from tabulate import tabulate

def roll_dice():
    """Simulate rolling a six-sided dice."""
    return random.randint(1, 6)

def display_dice(dice_value):
    """Display an ASCII art representation of a dice roll."""
    dice_art = {
        1: "🎲 [1]",
        2: "🎲 [2]",
        3: "🎲 [3]",
        4: "🎲 [4]",
        5: "🎲 [5]",
        6: "🎲 [6]",
    }
    return dice_art.get(dice_value, "[ ? ]")

def display_table(player_rolls, dealer_rolls, reveal_dealer=False):
    """Display the table of current rolls for the player and the dealer."""
    if reveal_dealer:
        dealer_display = [display_dice(dice) for dice in dealer_rolls]
        dealer_total_display = sum(dealer_rolls)
    else:
        dealer_display = [display_dice(dealer_rolls[0]), "[?]"]
        dealer_total_display = "[?]"

    table_data = [
        ["Player", " ".join(display_dice(dice) for dice in player_rolls), sum(player_rolls)],
        ["Dealer", " ".join(dealer_display), dealer_total_display]
    ]
    print(tabulate(table_data, headers=["Role", "Rolls", "Total"], tablefmt="fancy_grid"))

def dealer_action(dealer_rolls):
    """Simulate the dealer's actions based on standard rules."""
    dealer_total = sum(dealer_rolls)
    while dealer_total < 10:
        dealer_rolls.append(roll_dice())
        dealer_total = sum(dealer_rolls)
    return dealer_rolls

def log_game_result(player_rolls, dealer_rolls, outcome):
    """Log the result of each game into a JSON file, maintaining a list structure."""
    game_data = {
        'player_rolls': player_rolls,
        'dealer_rolls': dealer_rolls,
        'outcome': outcome  # "player", "dealer", or "tie"
    }
    try:
        with open('./output/game_logs.json', 'r') as file:
            # Attempt to read the existing data
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start a new list
        data = []
    
    # Append the new game data
    data.append(game_data)
    
    with open('output/game_logs.json', 'w') as file:
        json.dump(data, file, indent=4)

def play_round():
    player_rolls = [roll_dice(), roll_dice()]
    dealer_rolls = [roll_dice(), roll_dice()]
    display_table(player_rolls, dealer_rolls)

    while True:
        player_total = sum(player_rolls)
        if player_total == 13:
            display_table(player_rolls, dealer_rolls, reveal_dealer=True)
            print("🎉 13 👤 You win!")
            log_game_result(player_rolls, dealer_rolls, "player")
            return
        elif player_total > 13:
            display_table(player_rolls, dealer_rolls, reveal_dealer=True)
            print("💥 Bust. 🎩 Dealer wins.")
            log_game_result(player_rolls, dealer_rolls, "dealer")
            return

        decision = input("\nDo you want to hit? (y/n): ").lower()
        if decision == 'y':
            roll = roll_dice()
            player_rolls.append(roll)
        elif decision == 'n':
            break
        else:
            print("Invalid input. Please enter 'y' to hit or 'n' to stick.")
        display_table(player_rolls, dealer_rolls)

    # Dealer's turn
    dealer_rolls = dealer_action(dealer_rolls)
    display_table(player_rolls, dealer_rolls, reveal_dealer=True)
    dealer_total = sum(dealer_rolls)
    
    if dealer_total > 13:
        print("👤💰 You win! 🎩💥 Dealer bust.")
        outcome = "player"
    elif player_total > dealer_total:
        print("👤💰 You win!")
        outcome = "player"
    elif player_total == dealer_total:
        print("🤝 It's a tie.")
        outcome = "tie"
    else:
        print("🎩 Dealer wins!")
        outcome = "dealer"
    log_game_result(player_rolls, dealer_rolls, outcome)

# Play a round
play_round()
