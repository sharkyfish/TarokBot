import random

# --- Game Mechanics ---

def shuffle_and_deal(deck, num_players=4):
    random.shuffle(deck)
    talon = deck[:6]  # The first 6 cards form the talon
    hands = [deck[6 + i::num_players] for i in range(num_players)]
    return hands, talon


def sort_hand(hand):
    # Separate taroks and suited cards
    taroks = sorted([card for card in hand if card.suit == 'Tarok'], key=lambda c: int(c.rank))
    suited_cards = {suit: [] for suit in ['Clubs', 'Spades', 'Hearts', 'Diamonds']}
    
    # Sort suited cards and assign to the correct suit
    for card in hand:
        if card.suit != 'Tarok':
            suited_cards[card.suit].append(card)
    
    # Define custom order for face cards and use it when sorting suits
    face_card_order = {'Jack': 11, 'Knight': 12, 'Queen': 13, 'King': 14}
    
    # Sort each suit based on their specific rank orders
    for suit in suited_cards:
        if suit in ['Clubs', 'Spades']:
            suited_cards[suit] = sorted(
                suited_cards[suit],
                key=lambda c: int(c.rank) if c.rank.isdigit() else face_card_order[c.rank]
            )
        else:  # For Hearts and Diamonds
            # Define custom rank order with face cards above 1, 2, 3, 4
            rank_order_hearts_diamonds = {'1': 4, '2': 3, '3': 2, '4': 1} 
            suited_cards[suit] = sorted(
                suited_cards[suit],
                key=lambda c: rank_order_hearts_diamonds.get(c.rank, face_card_order[c.rank] if c.rank in face_card_order else int(c.rank))
            )

    # Combine taroks and suited cards back into a single hand
    sorted_hand = taroks + suited_cards['Clubs'] + suited_cards['Spades'] + suited_cards['Hearts'] + suited_cards['Diamonds']
    return sorted_hand


def bidding_phase(players): 
    # todo: Implement a bidding phase

    # For simplicity, assume the first player is the declarer
    declarer = players[0]
    return declarer


def play_trick(players, lead_player_index, print_trick=False):
    trick = []  # Cards played in the trick

    # Lead player plays a card
    lead_card = players[lead_player_index].choose_card_to_play(None)  # No lead suit for the first player
    trick.append((players[lead_player_index], lead_card))
    lead_suit = lead_card.suit  # Suit of the lead card

    # Each other player takes their turn
    for i in range(1, len(players)):
        player = players[(lead_player_index + i) % len(players)]
        card_to_play = player.choose_card_to_play(lead_suit)
        trick.append((player, card_to_play))

    # Determine the winner of the trick
    winner = determine_trick_winner(trick, lead_suit)
    winner.add_trick([card for _, card in trick])  # Add the cards to the winner's tricks_won

    if print_trick:
        # Print cards played in the trick
        for player, card in trick:
            print(f"{player.name} played: {card}")

    return winner


def determine_trick_winner(trick, lead_suit):
    # Separate the cards in the trick by lead suit and Taroks (trumps)
    lead_cards = [card for player, card in trick if card.suit == lead_suit]
    trumps = [card for player, card in trick if card.suit == 'Tarok']

    # Define custom rank order for each suit
    face_card_order = {'Jack': 11, 'Knight': 12, 'Queen': 13, 'King': 14}
    suit_rank_order = {
        'Clubs': {str(i): i for i in range(7, 11)},  # Ranks 7 to 10 for Clubs
        'Spades': {str(i): i for i in range(7, 11)},  # Ranks 7 to 10 for Spades
        'Hearts': {'4': 1, '3': 2, '2': 3, '1': 4},  # Ranks 4 to 1 for Hearts
        'Diamonds': {'4': 1, '3': 2, '2': 3, '1': 4} # Ranks 4 to 1 for Diamonds
    }

    # Add face cards to each suit's ranking order, so the King is highest in each suit
    for suit in suit_rank_order:
        suit_rank_order[suit].update(face_card_order)

    # Determine the winning card
    if trumps:
        # If there are trumps in the trick, the highest trump wins
        winning_card = max(trumps, key=lambda c: int(c.rank))
    else:
        # If no trumps, the highest card of the lead suit wins
        winning_card = max(lead_cards, key=lambda c: suit_rank_order[lead_suit][c.rank])

    # Find the player who played the winning card
    for player, card in trick:
        if card == winning_card:
            return player


def calculate_points(player):
    # Get all points from cards won in tricks
    card_values = [card.points for card in player.tricks_won]
    total_points = 0

    # Process full batches of three cards
    for i in range(0, len(card_values) - len(card_values) % 3, 3):

        batch_sum = sum(card_values[i:i+3])  # Sum points for each batch of three
        total_points += batch_sum - 2        # Subtract 2 from each batch's sum

    # Process remaining cards (1 or 2 cards left)
    remaining_cards = card_values[len(card_values) - len(card_values) % 3:]   
    remaining_sum = sum(remaining_cards)

    if remaining_sum > 0:
        total_points += max(remaining_sum - 1, 0)  # Subtract 1 point from the remaining sum, but not below 0

    return total_points