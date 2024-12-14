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
        self.total += card.get_value()
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

    def __getitem__(self, key):
        return self.cards[key]

    def __str__(self):
        return " ".join(map(str, self.cards)) + f" [{self.total}]"


class Player:
    option_map = {
        'h': 'hit',
        's': 'stand',
        'd': 'double',
        'p': 'split',
        'r': 'surrender'
    }

    display_option_map = {
        'hit': 'h',
        'stand': 's',
        'double': 'd',
        'split': 'p',
        'surrender': 'r'
    }

    def __init__(self, bankroll):
        self.bankroll = bankroll
        self.hands = []

    def new_round(self):
        self.hands = [Hand()]

    def move(self, hand, dealer_hand, legal_moves):
        print(f"Dealer's hand: {dealer_hand.cards[0]} ??")
        print(f"Your hand: {hand.get_string_for_player()}")
        while True:
            print("Options: ", end="")
            print(", ".join(f"{move} ({self.display_option_map[move]})"
                            for move in legal_moves))
            move = input("Enter your move: ").strip().lower()
            if move in self.option_map:
                if self.option_map[move] in legal_moves:
                    return self.option_map[move]
                else:
                    print("Invalid move")
            else:
                print("Invalid input")

    def get_bet(self):
        print(f"Bankroll: {self.bankroll}")
        bet = int(input("Enter your bet: "))
        print()
        return bet


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def new_round(self):
        self.hand = Hand()

    def move(self):
        pass
