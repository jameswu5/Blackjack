import numpy as np
from player import Player
from strategy import h17_strategy, s17_strategy


class RandomBot(Player):
    def __init__(self, bankroll, seed=None):
        super().__init__(bankroll)
        self.rng = np.random.default_rng(seed)

    def move(self, hand, dealer_hand, legal_moves):
        return self.rng.choice(legal_moves)

    def get_bet(self):
        return min(self.bankroll, 100)


class BasicStrategyBot(Player):
    def __init__(self, bankroll, observer, ruleset):
        super().__init__(bankroll)
        self.observer = observer

        if ruleset.threshold != 17:
            raise NotImplementedError("Only 17 threshold implemented")

        self.ruleset = ruleset
        self.strategy = s17_strategy if ruleset.stand_soft else h17_strategy
        self.unit_size = bankroll // 1000

    def move(self, hand, dealer_hand, legal_moves):
        dealer_value = dealer_hand.cards[0].get_value()

        total = hand.total

        if 'split' in legal_moves:
            first_card_value = hand[0].get_value()
            option = self.strategy['pairs'][first_card_value][dealer_value]
            if option == 'Y': return 'split'
            if option == 'M' and self.ruleset.das: return 'split'
            if option == 'R':
                return 'surrender' if 'surrender' in legal_moves else 'hit'

        table = 'soft' if hand.soft_aces else 'hard'
        option = self.strategy[table][total][dealer_value]
        if option == 'H': return 'hit'
        if option == 'S': return 'stand'
        if option == 'D':
            return 'double' if 'double' in legal_moves else 'hit'
        if option == 'F':
            return 'double' if 'double' in legal_moves else 'stand'
        if option == 'R':
            return 'surrender' if 'surrender' in legal_moves else 'hit'
        if option == 'V':
            return 'surrender' if 'surrender' in legal_moves else 'stand'

        raise ValueError(f'Invalid option: {option}')

    def get_bet(self):
        return self.unit_size


class CardCounter(BasicStrategyBot):
    def get_bet(self):
        true_count = self.observer.get_true_count()
        multipliers = [1, 2, 4, 8, 12, 16]
        true_count = max(0, min(true_count, len(multipliers) - 1))
        return self.unit_size * multipliers[true_count]
