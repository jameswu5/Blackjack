import random


class Card:
    suits = {
        'spades': '\u2660', 'hearts': '\u2665',
        'clubs': '\u2663', 'diamonds': '\u2666'
    }
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank}{Card.suits[self.suit]}'


class CardCollection:
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def __setitem__(self, position, value):
        self.cards[position] = value

    def pop(self):
        return self.cards.pop()

    def append(self, card):
        self.cards.append(card)

    def peek(self):
        return self.cards[-1]


class Shoe(CardCollection):
    def __init__(self, num_decks):
        super().__init__()
        self.num_decks = num_decks
        self.populate()

    def populate(self):
        for _ in range(self.num_decks):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.pop()


if __name__ == '__main__':
    pass
