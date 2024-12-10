import copy
import random
from game_mechanics import chosen_suit, calculate_points

class GameState:

    def __init__(self, ai_player, declarer, players, lead_player_index, talon, lead_suit, all_cards_played, trick, deck):
        self.players = [copy.deepcopy(player) for player in players]
        self.players_in_order = [self.players[(i + lead_player_index) % len(players)] for i in range(len(players))]
        self.declarer = declarer

        self.ai_player = None
        for player in self.players:
            if player.name == ai_player.name:
                self.ai_player = player

        self.trick = trick
        self.all_played_cards = all_cards_played
        self.talon = talon
        self.lead_suit = lead_suit

        self.known_cards = [(ai_player, card) for card in ai_player.hand]
        self.known_cards.extend(talon)
        self.known_cards.extend(all_cards_played)
        self.known_cards.extend(trick)

        self.unknown_cards = [card for card in deck if card not in self.known_cards]

        def guess_players_hands(cards: list, players: list, ai_player):
            random.shuffle(cards)

            players_with_unknown_hands = players.copy()
            players_with_unknown_hands.remove(ai_player)

            for player in players_with_unknown_hands:
                player.hand = []

            for i in range(len(cards)):
                player_index = i % len(players_with_unknown_hands)
                players_with_unknown_hands[player_index].hand.append(cards[i])

        guess_players_hands(self.unknown_cards, self.players, self.ai_player)

        def find_allies(players, declarer, chosen_suit):
            allies = [declarer]

            for player in players:
                if player == declarer:
                    continue

                for card in player.hand:
                    if card.rank == "King" and card.suit == chosen_suit:
                        allies.append(player)
                        return allies
                    
            return allies

        self.allies: Team = Team(
            name = "Allies",
            team_members = find_allies(self.players, self.declarer, chosen_suit))
        
        self.opponents: Team = Team(
            name = "Opponents",
            team_members = [player for player in self.players if player not in self.allies.team_members])

        self.active_player_index = 0
        self.active_player = self.players_in_order[self.active_player_index]

        self.winning_team = None

class Team:
    def __init__(self, name, team_members):
        self.name = name
        self.team_members = team_members
        self.tricks_won = [(player, card) for player in self.team_members for card in player.tricks_won]
        self.points = calculate_points([card[1] for card in self.tricks_won])