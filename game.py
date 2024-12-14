from card import Shoe
from ruleset import sr
from player import Hand, Player, Dealer

decks_in_shoe = 6
penetration = 0.75
reset_threshold = decks_in_shoe * 52 * (1 - penetration)

bankroll = 10000


class Game:
    def __init__(self, ruleset=sr):
        self.shoe = Shoe(num_decks=decks_in_shoe)
        self.ruleset = ruleset
        self.player = Player(bankroll=bankroll)
        self.dealer = Dealer()

    def simulate(self, max_rounds):
        for _ in range(max_rounds):
            self.play_round()

    def play_round(self):
        if len(self.shoe) < reset_threshold:
            self.shoe.reset()

        self.player.new_round()
        self.dealer.new_round()

        # Place bet
        bet = self.player.get_bet()
        self.player.hands[0].bet = bet
        self.player.bet = bet
        self.player.bankroll -= bet

        # Deal cards
        for _ in range(2):
            self.player.hands[0].add_card(self.shoe.deal())
            self.dealer.hand.add_card(self.shoe.deal())

        # Player's turn
        i = 0
        while i < len(self.player.hands):
            self.play_hand(self.player.hands[i])
            i += 1

        # Dealer's turn
        self.play_dealer()

        # Handle outcomes and payouts
        self.payout()

    def get_legal_moves_player(self, hand):
        moves = ['hit', 'stand']
        if self.ruleset.surrender:
            moves.append('surrender')
        if len(hand) == 2 and hand[0].rank == hand[1].rank:
            moves.append('split')
        if not (hand.split and not self.ruleset.das):
            moves.append('double')
        return moves

    def play_hand(self, hand):
        while hand.total < 21:
            move = self.player.move(hand, self.dealer.hand,
                                    self.get_legal_moves_player(hand))
            if move == 'hit':
                hand.add_card(self.shoe.deal())
            elif move == 'stand':
                break
            elif move == 'split':
                self.player.bet += hand.bet
                self.player.bankroll -= hand.bet
                hand.split = True
                new_hand = Hand(split=True)
                new_hand.add_card(hand.cards.pop())
                new_hand.bet = hand.bet
                hand.add_card(self.shoe.deal())
                new_hand.add_card(self.shoe.deal())
                self.player.hands.append(new_hand)
            elif move == 'surrender':
                hand.surrender = True
                break
            elif move == 'double':
                self.player.bet += hand.bet
                self.player.bankroll -= hand.bet
                hand.bet *= 2
                hand.add_card(self.shoe.deal())
                break
            else:
                raise ValueError(f'Invalid move for player: {move}')

    def play_dealer(self):
        while self.dealer.hand.total < 21:
            move = self.get_move_dealer()
            if move == 'hit':
                self.dealer.hand.add_card(self.shoe.deal())
            elif move == 'stand':
                break
            else:
                raise ValueError(f'Invalid move for dealer: {move}')

    def get_move_dealer(self):
        if self.dealer.hand.total < self.ruleset.threshold:
            return 'hit'
        elif self.dealer.hand.total == self.ruleset.threshold \
                and not self.ruleset.stand_soft and self.dealer.hand.soft_aces:
            return 'hit'
        else:
            return 'stand'

    def payout(self):
        payout = 0
        print()
        print("---Results---")

        dealer_total = self.dealer.hand.total
        print(f"Dealer:\n{self.dealer.hand}")

        print("Player:")
        for hand in self.player.hands:
            print(hand, end=" ")
            if hand.surrender:
                payout += hand.bet // 2
                print("(Surrender)")
            elif hand.total > 21:  # Bust
                print("(Bust)")
            elif hand.check_blackjack() \
                    and not self.dealer.hand.check_blackjack():
                pay = int(hand.bet * (1 + self.ruleset.blackjack_multiplier))
                payout += pay
                print("(Blackjack)")
            elif dealer_total > 21 or hand.total > dealer_total:  # Player wins
                payout += hand.bet * 2
                print("(Win)")
            elif hand.total == dealer_total:
                payout += hand.bet  # Push
                print("(Push)")
            elif hand.total < dealer_total:  # Player loses
                print("(Lose)")
            else:
                raise Exception("Something went wrong")
        print()
        net = payout - self.player.bet
        print(f"Bet: {self.player.bet} | Payout: {payout} | Net: {net}")
        self.player.bankroll += payout
        print()
