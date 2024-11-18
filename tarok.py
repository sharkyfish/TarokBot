from player import Player
from deck import Card, create_deck
from game_mechanics import shuffle_and_deal, sort_hand, bidding_phase, play_trick, determine_trick_winner, calculate_points
from ai_player import AIPlayer


# --- Main Game Loop ---
def start_game():

    # create the deck
    deck = create_deck()

    # create the players
    player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    players = [Player(name) for name in player_names]

    # shuffle and deal the deck
    hands, talon = shuffle_and_deal(deck)
    for i, player in enumerate(players):
        player.hand = hands[i]

    # sort the hands
    for player in players:
        player.hand = sort_hand(player.hand)

    # print the hands
    # for player in players:
    #     print(f"{player.name}: {player.hand}\n")


    # Bidding phase
    declarer = bidding_phase(players)
    print(f"{declarer.name} is the declarer.")


    # Play the game
    lead_player_index = 0 # The first player starts the game
    for _ in range(12):  # Each player plays 12 cards; 12 tricks in total

        winner = play_trick(players, lead_player_index, print_trick=False)
        # print(f"{winner.name} wins the trick.\n")
        lead_player_index = players.index(winner)


    # Calculate and print the points
    sum_points = 0
    for player in players:

        player_score = calculate_points(player)
        sum_points += player_score
        print(f"{player.name} scored {player_score} points.")

    print(f"\nTotal points: {sum_points}")


if __name__ == "__main__":
    start_game() 
