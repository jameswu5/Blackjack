class Hand:
    def __init__(self, split=False):
        self.cards = []
        self.total = 0
        self.soft_aces = 0
        self.split = split

    def add_card(self, card):
        self.cards.append(card)
        self.total += card.value()
        if card.rank == 'A':
            self.soft_aces += 1
        if self.total > 21 and self.soft_aces:
            self.total -= 10
            self.soft_aces -= 1

    def __str__(self):
        return ", ".join(map(str, self.cards)) \
            + f" ({self.total}{' soft' if self.soft_aces else ''})"


class Player:
    def __init__(self, bankroll):
        self.bankroll = bankroll
        self.hands = []

    def new_round(self):
        self.hands = [Hand()]

    def move(self):
        pass


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def new_round(self):
        self.hand = Hand()

    def move(self):
        pass
