import copy
import random
from game_mechanics import called_king

class GameState:

    def __init__(self, ai_player, declarer, players, lead_player_index, talon, lead_suit, all_cards_played, current_trick_cards, deck):
        self.players = [copy.deepcopy(player) for player in players]
        self.players_in_order = [self.players[(i + lead_player_index) % players.len()] for i in range(players)]
        self.declarer = declarer

        self.ai_player = None
        for player in self.players:
            if player.name == ai_player.name:
                self.ai_player = player

        self.current_trick_cards = current_trick_cards
        self.all_played_cards = all_cards_played
        self.talon = talon
        self.lead_suit = lead_suit

        self.known_cards = talon.extend(all_cards_played).extend(current_trick_cards)
        self.unknown_cards = [card for card in deck if card not in self.known_cards]

        def guess_players_hands(cards, players, ai_player):
            random.shuffle(cards)
            players_with_unknown_hands = players.remove(ai_player)

            for player in players_with_unknown_hands:
                player.hand = []

            for i in range(cards):
                player_index = i % players.len()
                players_with_unknown_hands[player_index].hand.append(cards[i])

        guess_players_hands(self.unknown_cards, self.players, self.ai_player)

        def find_allies(players, declarer, called_king):
            allies = [declarer]

            for player in players:
                if player == declarer:
                    continue

                for card in player.hand:
                    if called_king.suit == card.suit and called_king.rank == card.rank:
                        allies.append(player)
                        return allies
                    
            return allies

        self.allies = find_allies(self.players, self.declarer, called_king)
        self.opponents = [player for player in self.players if player not in self.allies]

        self.next_player = self.players_in_order[1]



