class Hand:
    def __init__(self, split=False):
        self.cards = []
        self.total = 0
        self.soft_aces = 0
        self.split = split
        self.surrender = False
        self.bet = 0

    def add_card(self, card):
        self.cards.append(card)
        self.total += card.value()
        if card.rank == 'A':
            self.soft_aces += 1
        if self.total > 21 and self.soft_aces:
            self.total -= 10
            self.soft_aces -= 1

    def check_blackjack(self):
        return len(self) == 2 and self.total == 21

    def get_string_for_player(self):
        return f"{str(self)}{' soft' if self.soft_aces else ''}"

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return ", ".join(map(str, self.cards)) + f" - {self.total}"


class Player:
    def __init__(self, bankroll):
        self.bankroll = bankroll
        self.hands = []

    def new_round(self):
        self.hands = [Hand()]

    def move(self, hand, dealer_hand, legal_moves):
        pass

    def get_bet(self):
        return 10


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def new_round(self):
        self.hand = Hand()

    def move(self):
        pass
