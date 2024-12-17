import numpy as np
from card import Shoe
from ruleset import sr
from player import Hand, Player, Dealer
from bot import RandomBot, BasicStrategyBot, CardCounter
from observer import Observer

decks_in_shoe = 6
penetration = 0.75
reset_threshold = decks_in_shoe * 52 * (1 - penetration)

bankroll = 10000


class Game:
    def __init__(self, player_type, ruleset=sr):
        self.shoe = Shoe(num_decks=decks_in_shoe)
        self.ruleset = ruleset
        self.observer = Observer(decks_in_shoe=decks_in_shoe)
        self.player = self.create_player(player_type)
        self.dealer = Dealer()

        # Game information (for plotting)
        self.round = 0
        self.player_bankroll = np.array([bankroll])
        self.true_count = np.array([0])
        self.new_shoes = np.array([0])
        self.win_stats = np.array([])

    def create_player(self, player_type):
        if player_type == "human":
            return Player(bankroll)
        if player_type == "random":
            return RandomBot(bankroll)
        if player_type == "basic":
            return BasicStrategyBot(bankroll, self.observer, self.ruleset)
        if player_type == "counter":
            return CardCounter(bankroll, self.observer, self.ruleset)

        raise ValueError(f"Invalid player type: {player_type}")

    def simulate(self, max_rounds, verbose=False):
        while self.round < max_rounds:
            self.play_round(verbose)
            self.player_bankroll = np.append(self.player_bankroll, self.player.bankroll)
            self.true_count = np.append(self.true_count, self.observer.get_true_count())

            if self.player.bankroll <= 0:
                print(f"Player is out of money after {self.round} rounds")
                break
            self.round += 1

    def play_round(self, verbose):
        if verbose:
            print("---New round---")
            print(f"Bankroll: {self.player.bankroll}")

        if len(self.shoe) < reset_threshold:
            self.shoe.reset()
            self.observer.reset()
            self.new_shoes = np.append(self.new_shoes, self.round)

        self.player.new_round()
        self.dealer.new_round()

        # Place bet
        bet = self.player.get_bet()
        self.player.hands[0].bet = bet
        self.player.bet = bet
        self.player.bankroll -= bet

        # Deal cards
        self.deal_card(self.player.hands[0])
        self.deal_card(self.player.hands[0])
        self.deal_card(self.dealer.hand)
        self.dealer.hand.add_card(self.shoe.deal())  # This card is not visible

        # If dealer has blackjack, end round
        if self.dealer.hand.check_blackjack():
            self.payout(verbose=verbose, show_dealer_hand=True)
            return

        # Player's turn
        i = 0
        while i < len(self.player.hands):
            self.play_hand(self.player.hands[i])
            i += 1

        # Dealer's turn
        if self.player.active_hands > 0:
            # Reveal dealer's hidden card
            self.observer.update(self.dealer.hand[1])
            self.play_dealer()

        # Handle outcomes and payouts
        self.payout(verbose=verbose, show_dealer_hand=self.player.active_hands > 0)

    def deal_card(self, target_hand):
        card = self.shoe.deal()
        target_hand.add_card(card)
        self.observer.update(card)

    def get_legal_moves_player(self, hand):
        moves = ['hit', 'stand']
        if self.ruleset.surrender and len(hand) == 2:
            moves.append('surrender')
        if self.player.bankroll >= hand.bet:
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
                self.deal_card(hand)
            elif move == 'stand':
                break
            elif move == 'split':
                self.player.bet += hand.bet
                self.player.bankroll -= hand.bet
                hand.split = True
                new_hand = Hand(split=True)
                new_hand.add_card(hand.cards.pop())
                new_hand.bet = hand.bet
                self.deal_card(hand)
                self.deal_card(new_hand)
                self.player.hands.append(new_hand)
                self.player.active_hands += 1
            elif move == 'surrender':
                hand.surrender = True
                self.player.active_hands -= 1
                break
            elif move == 'double':
                self.player.bet += hand.bet
                self.player.bankroll -= hand.bet
                hand.bet *= 2
                hand.add_card(self.shoe.deal())
                break
            else:
                raise ValueError(f'Invalid move for player: {move}')

        if hand.total > 21:
            self.player.active_hands -= 1

    def play_dealer(self):
        while self.dealer.hand.total < 21:
            move = self.get_move_dealer()
            if move == 'hit':
                self.deal_card(self.dealer.hand)
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

    def payout(self, verbose, show_dealer_hand=True):
        payout = 0

        output_string = "\n- Results -\n"

        dealer_total = self.dealer.hand.total
        if show_dealer_hand:
            output_string += f"Dealer:\n{self.dealer.hand}\n"
        else:
            output_string += f"Dealer:\n{self.dealer.hand.cards[0]} ??\n"

        output_string += "Player:\n"
        for hand in self.player.hands:
            output_string += str(hand) + " "
            if hand.surrender:
                payout += hand.bet // 2
                output_string += "(Surrender)\n"
            elif hand.total > 21:  # Bust
                output_string += "(Bust)\n"
            elif hand.check_blackjack() \
                    and not self.dealer.hand.check_blackjack():
                pay = int(hand.bet * (1 + self.ruleset.blackjack_multiplier))
                payout += pay
                output_string += "(Blackjack)\n"
            elif dealer_total > 21 or hand.total > dealer_total:  # Player wins
                payout += hand.bet * 2
                output_string += "(Win)\n"
            elif hand.total == dealer_total:
                payout += hand.bet  # Push
                output_string += "(Push)\n"
            elif hand.total < dealer_total:  # Player loses
                output_string += "(Lose)\n"
            else:
                raise Exception("Something went wrong")
        net = payout - self.player.bet
        self.win_stats = np.append(self.win_stats, max(-1, min(1, net)))
        self.player.bankroll += payout
        output_string += f"\nBet: {self.player.bet} | Payout: {payout} | Net: {net}\n\n"

        if verbose:
            print(output_string)
