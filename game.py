from card import Shoe
from ruleset import sr

decks_in_shoe = 6
penetration = 0.75


class Game:
    def __init__(self, ruleset=sr):
        self.shoe = Shoe(num_decks=decks_in_shoe)
        self.ruleset = ruleset
