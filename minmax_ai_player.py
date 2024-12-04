from player import Player
from game_state import GameState
import copy
from game_mechanics import determine_trick_winner
import random

class MinMaxAIPlayer(Player): # Inherit from the Player class

    def choose_card_to_play(self, lead_suit, deck, talon, all_cards_played, current_trick_cards, lead_player_index, players, declarer):
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
        game_state = GameState(self, declarer, players, lead_player_index, talon, lead_suit, all_cards_played, current_trick_cards, deck)

        def min_max(game_state: GameState):

            def play(game_state: GameState, player):

                def find_valid_cards(hand, lead_suit):
                    valid_cards = []

                    if lead_suit != None:

                        valid_cards = [card for card in hand if card.suit == lead_suit]

                        if valid_cards.len() == 0:
                            valid_cards = [card for card in hand if card.suit == "Tarok"]
                            
                    else:

                        valid_cards = hand

                    return valid_cards

                if game_state.current_trick_cards.len() >= 4:
                    return determine_trick_winner(game_state.current_trick_cards, game_state.lead_suit)

                game_state.next_player = game_state.players_in_order.index(player) + 1

                best_card = None
                valid_cards = find_valid_cards(player.hand, game_state.lead_suit)

                for card in valid_cards:
                    winner = play(current_trick_cards.append(card), game_state.next_player)

                if player in game_state.opponents:
                    if winner in game_state.opponents:
                        best_card = card
                else:
                    if winner in game_state.allies:
                        best_card = card

                best_card = best_card if best_card != None else random.choice(player.hand)

                return best_card
            
            return play(game_state, game_state.ai_player)
        
        return min_max(game_state)

        # MinMax Pseodo code
        # MinMax (GamePosition game)
        # {
        #     return MaxMove (game);
        # }
        # 
        # MaxMove (GamePosition game)
        # {
        #     if (GameEnded(game))
        #     {
        #         return EvalGameState(game);
        #     }
        #     else
        #     {
        #         best_move <- {};
        #         moves <- GenerateMoves(game);
        #         ForEach moves
        #         {
        #             move <- MinMove(ApplyMove(game));
        #             if (Value(move) > Value(best_move))
        #             {
        #                 best_move <- move;
        #             }
        #         }
        #         return best_move;
        #     }
        # }
        # 
        # MinMove (GamePosition game)
        # {
        #     best_move <- {};
        #     moves <- GenerateMoves(game);
        #     ForEach moves
        #     {
        #         move <- MaxMove(ApplyMove(game));
        #         if (Value(move) > Value(best_move))
        #         {
        #             best_move <- move;
        #         }
        #     }
        #     return best_move;
        # }

        return super().choose_card_to_play(lead_suit, deck, talon, all_cards_played, current_trick_cards) # change this later