classic = {
    '2': 1, '3': 1, '4': 1, '5': 1,
    '6': 1, '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1,
    'K': -1, 'A': -1
}

omega_ii = {
    '2': 1, '3': 1, '4': 2, '5': 2,
    '6': 2, '7': 1, '8': 0, '9': 0,
    '10': -2, 'J': -2, 'Q': -2,
    'K': -2, 'A': 0
}


class Observer:
    def __init__(self, decks_in_shoe, system='classic'):
        self.decks_in_shoe = decks_in_shoe
        self.count = 0
        self.cards_seen = 0
        self.count_value = self.get_count_system(system)

    def get_count_system(self, system):
        if system == 'classic':
            return classic
        if system == 'omega_ii':
            return omega_ii
        raise ValueError(f"Invalid system: {system}")

    def get_true_count(self):
        decks_remaining = self.decks_in_shoe - self.cards_seen / 52
        return int(round(self.count / decks_remaining))

    def update(self, card):
        self.cards_seen += 1
        self.count += self.count_value[card.rank]

    def reset(self):
        self.count = 0
        self.cards_seen = 0
