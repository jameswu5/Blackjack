from player import Player
import random


class RandomBot(Player):
    def __init__(self, bankroll):
        super().__init__(bankroll)

    def move(self, hand, dealer_hand, legal_moves):
        # Chooses randomly for now
        return random.choice(legal_moves)

    def get_bet(self):
        return min(self.bankroll, 100)


class CardCounter(Player):
    def __init__(self, bankroll, observer):
        super().__init__(bankroll)
        self.observer = observer

    def move(self, hand, dealer_hand, legal_moves):
        dealer_visible_card_rank = dealer_hand.cards[0].rank

        # Implement basic strategy
        raise NotImplementedError

    def get_bet(self):
        true_count = self.observer.get_true_count()
        raise NotImplementedError
