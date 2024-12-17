# Blackjack

It is common knowledge that the house always wins. That is to say, the casino has an edge over the gambler in all of their games, and Blackjack is no exception. The house edge on a regular game of blackjack is around 2%.

However, blackjack is actually beatable if we use information about cards that have already been visibly dealt. In essence, we keep track of how many low-valued cards have appeared compared to high-valued cards, and this technique is known as **card counting**. Such practice is detested by casinos and they make every effort to ban every card counter from their casinos, but here we won’t worry about that, since our objective is to show that with card counting we can play advantaged blackjack, that is blackjack but we have the edge instead.

This works by exploiting the fact that the dealer deals from a shoe, a set number of decks mixed together and shuffled (usually 6-8). There is also the penetration, which is how many cards are dealt before the whole shoe is reshuffled. So for example, if the shoe size is 8 decks and the penetration is 75%, 6 decks are dealt before the shoe is reshuffled. In general, the higher the penetration, the greater the advantage we have since our count is reset less regularly. How we can gain an edge is by betting big when the true count is high so it is more likely we win, and placing minimum bets when the true count is negative or negative.

We will use a simple card counting system, where cards of value 2-6 contribute +1 to our running count, 7-9 don’t contribute anything, and 10-A contribute -1 to the running count. The true count is computed by the quotient

$$
\textit{true count} = \frac{\textit{running count}}{\textit{decks remaining}}
$$

We will also employ what’s known as **basic strategy**, a well-researched set of optimal strategy (that is, optimises the expected value) on every possible situation based on your hand and the dealer’s upturned card.

We assume the rules of a soft 17 game, which is as follows:

- Dealer must stand on 17 or above, but they hit a soft 17
- Double after split is allowed
- Late surrender allowed
- Blackjack payout 2:1

By simulating this game for 1000 rounds, we obtain the bankroll plot (for seed 42):

![simulation](https://github.com/user-attachments/assets/886f59c8-02e5-46be-9e89-49e21fb63b6a)

We can see that our player does indeed make money. We can see that we have really capitalised on the high true count at around round 900, where we made a series of big bets which paid off leading to a high increase in our bankroll.

That was one of the more successful runs, and we find that the edge is in fact still not great and there is quite a bit of variance. But we can notice an improvement nonetheless compared to playing optimally with basic strategy (which reduces the casino edge to 0.5%). We simulate 1000 runs each with 1000 rounds to generate the histogram of our final bankrolls following different strategies:

![win_histogram](https://github.com/user-attachments/assets/278aa1cc-b192-450f-8a75-a7aa9c9e9219)

We can see that on average, following basic strategy leads to a loss in our bankroll whereas using card counting and adjusting our bet-sizes accordingly leads to a positive mean. This shows that we have indeed turned blackjack into our favour with the card-counting system.
