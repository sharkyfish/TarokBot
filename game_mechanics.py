import random


# Define the possible contracts in the game
CONTRACTS = [
    {"name": "klop", "score": -70, "description": "Avoid taking points; available to forehand only."},
    {"name": "three", "score": 10, "description": "Call a king; take 3 cards from the talon."},
    {"name": "two", "score": 20, "description": "Call a king; take 2 cards from the talon."},
    {"name": "one", "score": 30, "description": "Call a king; take 1 card from the talon."},
    {"name": "solo three", "score": 40, "description": "Play alone; take 3 cards from the talon."},
    {"name": "solo two", "score": 50, "description": "Play alone; take 2 cards from the talon."},
    {"name": "solo one", "score": 60, "description": "Play alone; take 1 card from the talon."},
    {"name": "beggar", "score": 70, "description": "Play alone; take no tricks; no bonuses."},
    {"name": "solo without", "score": 80, "description": "Play alone; no cards from the talon."},
    {"name": "open beggar", "score": 90, "description": "Play alone; take no tricks; declarer's cards exposed."},
    {"name": "colour valat without", "score": 125, "description": "Win all tricks; no cards from the talon."},
    {"name": "valat without", "score": 500, "description": "Win all tricks; no bonuses."}
]


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


def bidding_phase(players, dealer_index):
    """
    Implements the bidding phase and determines the next dealer and forehand.
    """
    # Determine the new dealer and forehand
    new_forehand_index = (dealer_index + 1) % len(players)  # Forehand is the next player in the rotation

    # Rotate players to asign priority
    rotated_players = players[new_forehand_index:] + players[:new_forehand_index]

    current_bid = None
    current_bidder = None
    consecutive_passes = 0
    endAuction = False

    print(f"\nStarting the bidding phase (Dealer: {rotated_players[-1].name}, Forehand: {rotated_players[0].name})...")

    # First round: Skip forehand initially
    first_round_players = rotated_players[1:] + [rotated_players[0]]

    while (consecutive_passes < len(players)) and not endAuction:
        for player in first_round_players:

            # End the auction if only one player remains
            if sum(not getattr(player, "has_passed", False) for player in rotated_players) == 1:
                endAuction = True
                break

            # Skip player if they have already passed
            if getattr(player, "has_passed", False):
                continue

            print(f"{player.name}'s turn to bid.", end=" ")
            
            if current_bid:
                print(f"Current highest bid: {current_bid['name']} ({current_bid['score']} points)")
            else:
                print("No bids yet.")
            
            # Determine valid bids
            if current_bid is None:
                valid_bids = CONTRACTS  # All contracts are valid if no one has bid yet
            
            elif rotated_players.index(player) < rotated_players.index(current_bidder):
                # Higher priority: can bid equal or higher
                valid_bids = [c for c in CONTRACTS if c["score"] >= current_bid["score"]]
            else:
                # Lower priority: must bid strictly higher
                valid_bids = [c for c in CONTRACTS if c["score"] > current_bid["score"]]

            # Player decides to bid or pass
            action = player.decide_bid(current_bid, valid_bids)

            if action == "pass":
                print(f"{player.name} passes.")
                player.has_passed = True
                consecutive_passes += 1
            else:
                print(f"{player.name} bids: {action['name']}")
                current_bid = action
                current_bidder = player
                consecutive_passes = 0  # Reset consecutive passes

    # Declare winner
    if current_bidder:
        print(f"\n{current_bidder.name} is the declarer with the bid: {current_bid['name']}")
    else:
        print("\nNo one bid. Forehand must choose a contract.")

    return current_bidder, current_bid


def call_king(declarer, talon, players):
    """
    Handles the process of calling a king and determining partnerships.
    """
    print(f"{declarer.name} must call a king.")
    
    # Declarer chooses a suit
    chosen_suit = declarer.choose_suit()
    print(f"{declarer.name} calls the King of {chosen_suit}.")
    
    # Search for the king in players' hands and the talon
    called_king = None
    partner = None
    for player in players:
        if player != declarer:  # Skip declarer
            for card in player.hand:
                if card.rank == "King" and card.suit == chosen_suit:
                    partner = player
                    called_king = card
                    break
            if partner:
                break
    
    # Check if the called king is in the talon
    if not partner:
        for card in talon:
            if card.rank == "King" and card.suit == chosen_suit:
                print(f"The King of {chosen_suit} is in the talon. {declarer.name} plays alone.")
                return None  # Declarer plays alone

    # Partner found
    if partner:
        print(f"{partner.name} is the partner of {declarer.name}, holding the King of {chosen_suit}.")
        return partner
    
    # Declarer called their own king (plays alone)
    print(f"{declarer.name} called their own King of {chosen_suit}. {declarer.name} plays alone.")
    return None  # Declarer plays alone


def exchange_with_talon(declarer, talon, contract):
    """
    Handles the process of exchanging cards with the talon.
    """
    print(f"{declarer.name} is exchanging cards with the talon.")
    
    # Divide the talon based on the contract
    if contract["name"] == "three":
        talon_sets = [talon[:3], talon[3:]]
    elif contract["name"] == "two":
        talon_sets = [talon[:2], talon[2:4], talon[4:]]
    elif contract["name"] == "one":
        talon_sets = [[card] for card in talon]  # Individual cards
    else:
        print("This contract does not allow exchanging with the talon.")
        return

    # Display talon sets to the declarer
    print("Talon sets:")
    for i, talon_set in enumerate(talon_sets):
        print(f"Set {i + 1}: {talon_set}")

    # Declarer chooses a set
    chosen_set_index = declarer.choose_talon_set(len(talon_sets)) 
    chosen_set = talon_sets[chosen_set_index - 1]
    print(f"{declarer.name} chooses Set {chosen_set_index}: {chosen_set}")

    # Add chosen cards to declarer's hand
    declarer.hand.extend(chosen_set)

    # Discard cards
    discard_count = len(chosen_set)
    print(f"{declarer.name} must discard {discard_count} cards.")
    discarded_cards = declarer.discard_cards(discard_count) 
    print(f"{declarer.name} discards: {discarded_cards}")

    # Remaining talon cards go to opponents
    opponents_talon = [
        card
        for i, talon_set in enumerate(talon_sets)
        if i != chosen_set_index - 1  # Exclude the chosen set
        for card in talon_set  # Iterate through the cards in each unchosen set
    ]
    print(f"Remaining talon cards go to opponents: {opponents_talon}")

    return opponents_talon


def play_trick(players, lead_player_index, deck, talon, all_cards_played, print_trick=False):
    trick = []  # Cards played in the trick

    # Lead player plays a card
    lead_card = players[lead_player_index].choose_card_to_play(None, deck, talon, all_cards_played, trick)  # No lead suit for the first player
    trick.append((players[lead_player_index], lead_card))
    lead_suit = lead_card.suit  # Suit of the lead card

    # Each other player takes their turn
    for i in range(1, len(players)):
        player = players[(lead_player_index + i) % len(players)]
        card_to_play = player.choose_card_to_play(lead_suit, deck, talon, all_cards_played, trick)
        trick.append((player, card_to_play))

    # Determine the winner of the trick
    winner = determine_trick_winner(trick, lead_suit)
    winner.add_trick([card for _, card in trick])  # Add the cards to the winner's tricks_won

    # Update the list of all cards played in the game
    all_cards_played.extend([card for _, card in trick])

    if print_trick:
        # Print cards played in the trick
        for player, card in trick:
            print(f"{player.name} played: {card}")

    return winner, all_cards_played


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


def calculate_points(won_cards):
    # Get all points from cards won in tricks
    card_values = [card.points for card in won_cards]
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