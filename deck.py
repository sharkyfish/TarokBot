# --- Card Class and Deck Creation ---
class Card:

    def __init__(self, suit, rank, points):
        self.suit = suit
        self.rank = rank
        self.points = points


    def __repr__(self):
        return f"{self.rank} of {self.suit}"


def create_deck():
    suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    
    # Define points for face cards common to all suits
    face_cards = [('King', 5), ('Queen', 4), ('Knight', 3), ('Jack', 2)]
    
    # Define numbered cards for each suit
    numbered_cards = {
        'Clubs': [('10', 1), ('9', 1), ('8', 1), ('7', 1)],
        'Spades': [('10', 1), ('9', 1), ('8', 1), ('7', 1)],
        'Hearts': [('1', 1), ('2', 1), ('3', 1), ('4', 1)],  # 1 is the highest in Hearts
        'Diamonds': [('1', 1), ('2', 1), ('3', 1), ('4', 1)]  # 1 is the highest in Diamonds
    }
    
    # Create the deck for the suited cards
    deck = []
    for suit in suits:
        # Add face cards for each suit
        for rank, points in face_cards:
            deck.append(Card(suit, rank, points))
        
        # Add numbered cards based on the specific suit
        for rank, points in numbered_cards[suit]:
            deck.append(Card(suit, rank, points))

    # Add taroks with specific points for 1, 21, and 22
    taroks = [(str(i), 5 if i in {1, 21, 22} else 1) for i in range(1, 23)]
    deck.extend([Card('Tarok', rank, points) for rank, points in taroks])
    
    return deck