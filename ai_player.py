from player import Player

class AIPlayer(Player): # Inherit from the Player class

    def choose_card_to_play(self, lead_suit, deck, talon, all_cards_played, current_trick_cards, lead_player_index, players):
        # Implement AI-specific decision logic here

        return super().choose_card_to_play(self, lead_suit, deck, talon, all_cards_played, current_trick_cards) # change this later
    

    
