from player import Player

class AIPlayer(Player): # Inherit from the Player class

    def choose_card_to_play(self, lead_suit, deck, talon, all_cards_played, current_trick_cards):
        """
        Decides which card to play based on the lead suit and available game state.
        Parameters:
            - lead_suit: Suit of the lead card in the current trick (None if this player is the lead).
            - deck: The complete deck of cards in the game.
            - talon: Cards from the talon.
            - all_cards_played: All cards played in previous tricks.
            - current_trick_cards: Cards already played in the current trick.
        """

        # Implement AI-specific decision logic here

        return super().choose_card_to_play(lead_suit, deck, talon, all_cards_played, current_trick_cards) # change this later
    

    
