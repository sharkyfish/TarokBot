import random

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tricks_won = []
        self.has_passed = False  # Track if the player has passed during bidding

    
    def decide_bid(self, current_bid, valid_bids):
        """
        Decide whether to bid or pass. Only considers bids 'one' and 'two'
        """
        # Filter valid bids to only include 'one' and 'two'
        simplified_bids = [bid for bid in valid_bids if bid["name"] in ["one", "two"]]

        if not simplified_bids or random.random() > 0.5:
            # Pass if no valid bids or randomly decides to pass
            return "pass"
        else:
            # Randomly select from the simplified valid bids
            return random.choice(simplified_bids)
        
    
    def choose_suit(self):
        """
        Randomly chooses a suit for calling the king.
        """
        suit_choices = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
        chosen_suit = random.choice(suit_choices)

        return chosen_suit


    def choose_talon_set(self, num_sets):
        """
        Randomly chooses a set of cards from the talon.
        """
        chosen_set_index = random.randint(1, num_sets)  # Talon sets are 1-indexed
        return chosen_set_index


    def discard_cards(self, num_to_discard):
        """
        Randomly discards the specified number of cards from the player's hand,
        ensuring high-value cards (e.g., kings, trula cards) are not discarded.
        """
        # High-value cards to protect
        protected_cards = [card for card in self.hand if 
                        card.rank == "King" or 
                        (card.suit == "Tarok" and card.rank in {"1", "21", "22"})]
        
        # Cards eligible for discard
        discardable_cards = [card for card in self.hand if card not in protected_cards]   
        discarded = random.sample(discardable_cards, num_to_discard)
        
        # Remove the discarded cards from the hand and add them to the winning tricks pile
        for card in discarded:
            self.tricks_won.append(card)
            self.hand.remove(card)
        
        return discarded


    def choose_card_to_play(lead_suit, deck, talon, all_cards_played, current_trick_cards):
        """
        Decides which card to play based on the lead suit and available game state.
        Parameters:
            - lead_suit: Suit of the lead card in the current trick (None if this player is the lead).
            - deck: The complete deck of cards in the game.
            - talon: Cards from the talon.
            - all_cards_played: All cards played in previous tricks.
            - current_trick_cards: Cards already played in the current trick.
        """
        if lead_suit is None:
            # If this player is leading the trick, they can choose any card
            card_to_play = random.choice(self.hand) # Randomly choose a card
        else:
            # Try to follow the lead suit if possible
            card_to_play = next((card for card in self.hand if card.suit == lead_suit), None)

            if not card_to_play:
                # If no lead suit, play a Tarok if available
                card_to_play = next((card for card in self.hand if card.suit == 'Tarok'), None)

            if not card_to_play:
                # If no Tarok or lead suit, play any card
                card_to_play = self.hand[0]

        # Remove the chosen card from the hand
        self.hand.remove(card_to_play)
        return card_to_play


    def add_trick(self, trick):
        """Adds all cards from a won trick to the player's tricks."""
        self.tricks_won.extend(trick)

