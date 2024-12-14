import random


class Card:
    suits = {
        'spades': '\u2660', 'hearts': '\u2665',
        'clubs': '\u2663', 'diamonds': '\u2666'
    }
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    value = {
        '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank}{Card.suits[self.suit]}'

    def value(self):
        return Card.value[self.rank]


class Shoe():
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.reset()

    def __len__(self):
        return len(self.cards)

    def reset(self):
        self.cards = []
        self.populate()

    def populate(self):
        for _ in range(self.num_decks):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self.cards.append(Card(rank, suit))
        random.shuffle(self.cards)

    def deal(self):
        return self.pop()


if __name__ == '__main__':
    pass
