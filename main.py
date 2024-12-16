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
    for i in g.new_shoes:
        plt.axvline(i, color='grey', linestyle='--', alpha=0.5)
    plt.xlabel('Round')
    plt.ylabel('True Count')

    plt.tight_layout()
    plt.show()


def plot_simulation_together(rounds=1000):
    g = Game()
    g.simulate(rounds)

    fig, ax1 = plt.subplots(figsize=(10, 4))

    ax1.set_xlabel('Round')
    ax1.set_ylabel('Bankroll')
    ax1.plot(g.player_bankroll, color='blue', alpha=0.6, label='Bankroll')
    ax1.tick_params(axis='y')
    plt.legend()

    ax2 = ax1.twinx()
    ax2.set_ylabel('True Count')
    ax2.plot(g.true_count, color='purple', alpha=0.6, label='True Count')
    ax2.axhline(0, linestyle='--', color='grey', alpha=0.3)
    ax2.tick_params(axis='y')

    plt.title('Player Bankroll and True Count')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_simulation_together()
