from player import Player
import random


class Bot(Player):
    def __init__(self, bankroll):
        super().__init__(bankroll)

    def move(self, hand, dealer_hand, legal_moves):
        # Chooses randomly for now
        return random.choice(legal_moves)

    def get_bet(self):
        return min(self.bankroll, 100)
