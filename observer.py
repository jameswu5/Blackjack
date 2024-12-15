class Observer:
    count_value = {
        '2': 1, '3': 1, '4': 1, '5': 1,
        '6': 1, '7': 0, '8': 0, '9': 0,
        '10': -1, 'J': -1, 'Q': -1,
        'K': -1, 'A': -1
    }

    def __init__(self, decks_in_shoe):
        self.decks_in_shoe = decks_in_shoe
        self.count = 0
        self.cards_seen = 0

    def get_true_count(self):
        decks_remaining = self.decks_in_shoe - self.cards_seen / 52
        return self.count / decks_remaining

    def update(self, card):
        self.cards_seen += 1
        self.count += self.count_value[card.rank]
