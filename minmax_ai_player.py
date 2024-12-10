from player import Player
from game_state import GameState
from game_mechanics import determine_trick_winner, calculate_points
import random
import copy

class MinMaxAIPlayer(Player): # Inherit from the Player class

    def choose_card_to_play(self, lead_suit, deck, talon, all_cards_played, trick, lead_player_index, players, declarer):
        """
        Decides which card to play based on the lead suit and available game state.
        Parameters:
            - lead_suit: Suit of the lead card in the current trick (None if this player is the lead).
            - deck: The complete deck of cards in the game.
            - talon: Cards from the talon.
            - all_cards_played: All cards played in previous tricks.
            - trick: Cards already played in the current trick.
        """
        # Implement AI-specific decision logic here
        game_state = GameState(
            ai_player = self,
            declarer = declarer,
            players = players,
            lead_player_index = lead_player_index,
            talon = talon,
            lead_suit = lead_suit,
            all_cards_played = all_cards_played,
            trick = trick,
            deck = deck)
        
        self.game = 0

        def min_max(game_state: GameState):

            def find_valid_cards(hand, lead_suit):
                if lead_suit == None:
                    return hand
                    
                valid_cards = [card for card in hand if card.suit == lead_suit]
                    
                if len(valid_cards) == 0:
                    valid_cards = [card for card in hand if card.suit == "Tarok"]

                if len(valid_cards) == 0:
                    return hand

                return valid_cards

            def trick_finished_upkeap(game_state: GameState):
                self.game += 1
                #print("Game: " + str(self.game) +" Cards in trick: " + str([card[1] for card in game_state.trick]))
                
                winner = determine_trick_winner(game_state.trick, game_state.lead_suit)
                game_state.winning_team = game_state.allies if winner in game_state.allies.team_members else game_state.opponents
                game_state.winning_team.tricks_won.extend(game_state.trick)
                game_state.winning_team.points = calculate_points([card[1] for card in game_state.winning_team.tricks_won])

                if len(game_state.active_player.hand) == 0:
                    return (None, game_state)
                    


            def play(game_state: GameState):
                # If the trick is over, determine who won and
                # return the game state and the best card to play
                if len(game_state.trick) >= 4:
                    
                    self.game += 1
                    #print("Game: " + str(self.game) +" Cards in trick: " + str([card[1] for card in game_state.trick]))
                    
                    winner = determine_trick_winner(game_state.trick, game_state.lead_suit)
                    game_state.winning_team = game_state.allies if winner in game_state.allies.team_members else game_state.opponents
                    game_state.winning_team.tricks_won.extend(game_state.trick)
                    game_state.winning_team.points = calculate_points([card[1] for card in game_state.winning_team.tricks_won])

                    return (None, game_state)
                else: 
                    game_state.active_player = game_state.players_in_order[game_state.active_player_index]

                greatest_point_delta = 0
                valid_cards = find_valid_cards(game_state.active_player.hand, game_state.lead_suit)
                best_card = random.choice(valid_cards) #TODO: Find lowest value card

                for card in valid_cards:

                    next_state = copy.deepcopy(game_state)
                    next_state.lead_suit = card.suit if next_state.lead_suit == None else next_state.lead_suit

                    next_state.trick.append((game_state.active_player, card))
                    next_state.active_player_index += 1

                    next_state = play(next_state)[1]

                    point_delta = 0

                    if game_state.active_player in game_state.opponents.team_members:
                        point_delta = next_state.opponents.points - next_state.allies.points
                    else:
                        point_delta = next_state.allies.points - next_state.opponents.points

                    if point_delta > greatest_point_delta:
                        greatest_point_delta = point_delta
                        best_card = card
                    elif point_delta == greatest_point_delta:
                        #TODO: find card with lowest rank
                        #TODO: find card with lowest point score if losing, highest point score if winning
                        best_card = best_card
                    
                return (best_card, game_state)

            return play(game_state)[0]
        
        return min_max(game_state)

        return super().choose_card_to_play(lead_suit, deck, talon, all_cards_played, trick) # change this later