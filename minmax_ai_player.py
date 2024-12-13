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
        # Create gamestate object to monitor the state of the game 
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
        
        # Debug Code
        self.game = 0
        self.trick = 0

        self.max_depth = 11

        def min_max(game_state: GameState):

            def find_valid_cards(hand, lead_suit):
                '''
                Returns a list of the cards from the players hand that match the lead suit.
                If none match returns a list of trump cards from the players hand.
                If the player has no trump cards, returns the players entire hand.
                '''
                if lead_suit == None:
                    return hand
                    
                valid_cards = [card for card in hand if card.suit == lead_suit]
                    
                if len(valid_cards) == 0:
                    valid_cards = [card for card in hand if card.suit == "Tarok"]

                if len(valid_cards) == 0:
                    return hand

                return valid_cards

            def trick_finished_upkeap(game_state: GameState):
                '''
                Determines who won the trick, distributes cards to the winners,
                resets the trick variable and checks if the game is over
                '''                
                def assign_trick():
                    '''
                    Determine trick winner and assign winning team trick cards
                    '''
                    trick_winner = determine_trick_winner(game_state.trick, game_state.lead_suit)
                    winning_team = game_state.opponents

                    for player in game_state.allies.team_members:
                        if trick_winner.name == player.name:
                            winning_team = game_state.allies
                            break
                
                    winning_team.tricks_won.extend(game_state.trick)

                    return trick_winner

                game_state.depth += 1

                trick_winner = assign_trick()

                # Debug Code
                #self.trick += 1
                #print("Trick: " + str(self.trick))
                #print(trick_winner.name + " wins the trick")
                #print(" Cards in trick: " + str([(card[0].name, card[1]) for card in game_state.trick]))

                # Empty trick variable for next round and set the lead suit to None
                game_state.trick = []
                game_state.lead_suit = None

                # Check if the game is over
                if len(game_state.active_player.hand) == 1:
                    
                    # Play the final trick
                    game_state.lead_suit = game_state.active_player.hand[0].suit

                    for player in game_state.players:
                        game_state.trick.append((player, player.hand[0]))

                    assign_trick()

                    game_state.is_game_over = True
                    return

                # Find the player order for the next trick
                game_state.active_player_index = 0
                game_state.reorder_players(trick_winner)

            def game_end_upkeap(game_state: GameState):
                '''
                Calculate the scores of the teams, along with the winning team
                '''
                game_state.allies.points = calculate_points([card[1] for card in game_state.allies.tricks_won])
                game_state.opponents.points = calculate_points([card[1] for card in game_state.opponents.tricks_won])

                if game_state.allies.points > game_state.opponents.points:
                    game_state.winning_team = game_state.allies
                else:
                    game_state.winning_team = game_state.opponents

                # Debug code
                #self.game += 1
                #print("Game: " + str(self.game) +
                #      " Winners: " + game_state.winning_team.name +
                #      " Points: " + str(game_state.winning_team.points))

                return (None, game_state)

            def max_depth_upkeap(game_state: GameState):
                '''
                Calculate the scores of the teams, the strenght of the AI players current hand
                along with the currently leading team
                '''
                game_state.allies.points = calculate_points([card[1] for card in game_state.allies.tricks_won])
                game_state.opponents.points = calculate_points([card[1] for card in game_state.opponents.tricks_won])

                if game_state.allies.points > game_state.opponents.points:
                    game_state.winning_team = game_state.allies
                else:
                    game_state.winning_team = game_state.opponents

                #TODO: Calculate the strenth of the players hand

                return (None, game_state)

            def play(game_state: GameState):
                # If trick is over, run upkeap
                if len(game_state.trick) >= 4: trick_finished_upkeap(game_state)

                # If the game is over, return final score
                if game_state.is_game_over: return game_end_upkeap(game_state)

                if game_state.depth > self.max_depth: return max_depth_upkeap(game_state)

                # Determine the next player
                game_state.active_player = game_state.players_in_order[game_state.active_player_index]

                # Find the cards the player is allowed to play
                valid_cards = find_valid_cards(game_state.active_player.hand, game_state.lead_suit)
                best_card = min(valid_cards, key= lambda c: c.points)

                # Determine what card leads to the best possible outcome for the game
                greatest_point_delta = 0

                for card in valid_cards:
                    # Create a copy of the game state to represent the next node in the game tree
                    # and determine the lead suit of the trick
                    next_state = copy.deepcopy(game_state)
                    next_state.lead_suit = card.suit if next_state.lead_suit == None else next_state.lead_suit

                    next_state.trick.append((game_state.active_player, card))

                    # Remove the played card from the player hand
                    for card_in_hand in next_state.active_player.hand:
                        if card_in_hand.suit == card.suit and card_in_hand.rank == card.rank:
                            next_state.active_player.hand.remove(card_in_hand)
                    
                    next_state.active_player_index += 1

                    #Play out the next state
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