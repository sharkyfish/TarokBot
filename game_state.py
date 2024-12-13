import copy
import random
from game_mechanics import get_chosen_suit, calculate_points

class GameState:

    def __init__(self, ai_player, declarer, players, lead_player_index, talon, lead_suit, all_cards_played, trick, deck):
        # Record players, their order, the declarer, and the AI
        self.players = [copy.deepcopy(player) for player in players]
        self.players_in_order = [self.players[(i + lead_player_index) % len(self.players)] for i in range(len(self.players))]
        
        self.declarer = None
        self.ai_player = None
        for player in self.players:
            if player.name == ai_player.name:
                self.ai_player = player
            elif player.name == declarer.name:
                self.declarer = player

        # Record the current trick in progress, as well as other card info
        self.trick = []
        for card in trick:
            for player in self.players:
                if card[0].name == player.name:
                    self.trick.append((player, card[1]))
        
        self.all_played_cards = all_cards_played
        self.talon = talon
        self.lead_suit = lead_suit

        # Record cards known the AI knows where are
        self.known_cards = [card for card in ai_player.hand]

        self.known_cards.extend(talon)
        self.known_cards.extend([card[1] for card in all_cards_played])
        self.known_cards.extend([card[1] for card in trick])
        
        self.unknown_cards = []

        def find_unknown_cards():
            '''
            Record the cards the AI does not know where are
            '''
            for card in deck:
                card_known = False
                for known_card in self.known_cards:
                    if card.suit == known_card.suit and card.rank == known_card.rank:
                        card_known = True
                    
                if card_known: continue
                self.unknown_cards.append(card)

        find_unknown_cards()

        def guess_players_hands(cards: list, players: list, ai_player):
            '''
            Randomly deal all unknown cards to players other than the AI
            '''
            random.shuffle(cards)

            players_with_unknown_hands = players.copy()
            players_with_unknown_hands.remove(ai_player)

            for player in players_with_unknown_hands:
                player.hand = []

            for i in range(len(cards)):
                player_index = i % len(players_with_unknown_hands)
                players_with_unknown_hands[player_index].hand.append(cards[i])

        guess_players_hands(self.unknown_cards, self.players, self.ai_player)

        # Split the players into teams
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
        
        print(get_chosen_suit())

        self.allies: Team = Team(
            name = "Allies",
            team_members = find_allies(self.players, self.declarer, get_chosen_suit()))

        self.opponents: Team = Team(
            name = "Opponents",
            team_members = [player for player in self.players if player not in self.allies.team_members])

        # Record the current player whos turn it is
        self.active_player_index = self.players_in_order.index(self.ai_player)
        self.active_player = self.players_in_order[self.active_player_index]

        self.winning_team = None

        self.is_game_over = False

        self.depth = 0

    def reorder_players(self, trick_winner):
        '''
        Reorders the players based on the winner of the last trick
        '''
        lead_player_index = 0

        for player in self.players:
            if player.name == trick_winner.name:
                lead_player_index = self.players.index(player)
                break

        self.players_in_order = [self.players[(i + lead_player_index) % len(self.players)] for i in range(len(self.players))]

class Team:
    def __init__(self, name, team_members):
        self.name = name
        self.team_members = team_members
        self.tricks_won = [(player, card) for player in self.team_members for card in player.tricks_won]
        self.points = calculate_points([card[1] for card in self.tricks_won])