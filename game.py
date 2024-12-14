from card import Shoe
from ruleset import sr
from player import Player, Dealer

decks_in_shoe = 6
penetration = 0.75
reset_threshold = decks_in_shoe * 52 * (1 - penetration)


class Game:
    def __init__(self, ruleset=sr):
        self.shoe = Shoe(num_decks=decks_in_shoe)
        self.ruleset = ruleset
        self.player = Player(bankroll=1000)
        self.dealer = Dealer()

    def simulate(self, max_rounds):
        for _ in range(max_rounds):
            self.play_round()

    def play_round(self):
        if len(self.shoe) < reset_threshold:
            self.shoe.reset()

        self.player.new_round()
        self.dealer.new_round()

        # Deal cards
        for _ in range(2):
            self.player.hands[0].add_card(self.shoe.deal())
            self.dealer.hand.add_card(self.shoe.deal())

        # Player's turn
        for i in range(len(self.player.hands)):
            pass

        # Dealer's turn
        pass

        # Handle outcomes and payouts
        pass
