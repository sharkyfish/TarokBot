from player import Player
from deck import Card, create_deck
from game_mechanics import shuffle_and_deal, sort_hand, bidding_phase, play_trick, determine_trick_winner, calculate_points, call_king, exchange_with_talon, CONTRACTS
from ai_player import AIPlayer


# --- Main Game Loop ---
def play_one_game(deck, players, dealer_index):

    # 1. shuffle and deal the deck
    #########################################################################################
    hands, talon = shuffle_and_deal(deck)
    for i, player in enumerate(players):
        player.hand = hands[i]
        # clear the winning tricks pile for each player
        player.tricks_won = []

    # sort the hands
    for player in players:
        player.hand = sort_hand(player.hand)

    # print the hands
    # for player in players:
    #     print(f"{player.name}: {player.hand}\n")


    # 2. Bidding phase
    #########################################################################################
    declarer, bid = bidding_phase(players, dealer_index)
    # Reset the "has_passed" attribute for the next game
    for player in players:
        player.has_passed = False

    if not bid:
        # TODO: Implement logic for the forehand to choose a contract

        declarer = players[dealer_index]
        bid = CONTRACTS[2]  # Dummy contract if no valid bids
    

    # 3. Call the king and exchange cards with the talon
    #########################################################################################
    # Call the king if the contract is one, two, or three
    if bid and bid["name"] in ["one", "two", "three"]:
        partner = call_king(declarer, talon, players)
    else:
        partner = None

    # Exchange with the talon if the contract allows it
    opponents_talon = exchange_with_talon(declarer, talon, bid)

    # Add remaining talon cards to one of the opponents' winning tricks pile
    for player in players:
        if player != declarer and player != partner:
            player.tricks_won.extend(opponents_talon)
            break # Only one opponent gets the remaining talon cards


    # 4. Play the game
    #########################################################################################

    # Track which cards have been played so far
    all_cards_played = []

    lead_player_index = (dealer_index + 1) % len(players) # forehand leads the first trick
    for _ in range(12):  # Each player plays 12 cards; 12 tricks in total

        winner, all_cards_played = play_trick(players, lead_player_index, deck, talon, all_cards_played, print_trick=False)
        # print(f"{winner.name} wins the trick.\n")
        lead_player_index = players.index(winner)


    # 5. Combine winning tricks and calculate points
    #########################################################################################
    # Separate teams
    declarer_team = [declarer]
    if partner:
        declarer_team.append(partner)

    opponents_team = [player for player in players if player not in declarer_team]

    # Combine tricks for each team
    declarer_team_tricks = [card for player in declarer_team for card in player.tricks_won]
    opponents_team_tricks = [card for player in opponents_team for card in player.tricks_won]

    # Calculate points for both teams
    declarer_team_score = calculate_points(declarer_team_tricks)
    opponents_score = calculate_points(opponents_team_tricks)

    # Total points
    sum_points = declarer_team_score + opponents_score

    # Print results
    print(f"\nTotal points: {sum_points}")
    print(f"Declarer's team score: {declarer_team_score}")
    print(f"Opponents' score: {opponents_score}")

    # Determine the winning team
    if declarer_team_score >= opponents_score:
        print(f"\nDeclarer's team wins the game!")
    else:
        print(f"\nOpponents win the game!")

    return declarer_team_score



if __name__ == "__main__":

    # create the deck
    deck = create_deck()

    # create the players
    player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    players = [AIPlayer(name) for name in player_names] # AI players from the AIPlayer class
    
    # Initial dealer (first game)
    dealer_index = 0 

    # Simulate multiple games
    for game_number in range(1):  # Simulate games

        print(f"\n=== Game {game_number + 1} ===")

        declarer_team_score = play_one_game(deck, players, dealer_index) # Play one game

        dealer_index = (dealer_index + 1) % len(players)  # Rotate the dealer
        print("\n---\n")
        
