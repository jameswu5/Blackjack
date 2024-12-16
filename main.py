import matplotlib.pyplot as plt
from game import Game


def plot_simulation(rounds=1000):
    g = Game()
    g.simulate(rounds)

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.title('Player Bankroll')
    plt.plot(g.player_bankroll)
    plt.xlabel('Round')
    plt.ylabel('Bankroll')

    plt.subplot(2, 1, 2)
    plt.title('True Count')
    plt.plot(g.true_count)
    plt.axhline(0, linestyle='--')
    plt.xlabel('Round')
    plt.ylabel('True Count')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_simulation()
