import random

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tricks_won = []


    def choose_card_to_play(self, lead_suit):
        """
        Decides which card to play based on the lead suit and available cards.
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

