import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
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


def plot_win_data():
    g = Game()
    g.simulate(1000)

    grouped_stats = defaultdict(lambda: [0, 0, 0])
    for tc, ws in zip(g.true_count, g.win_stats):
        grouped_stats[tc][int(ws)+1] += 1

    true_counts = sorted(grouped_stats.keys())
    win_stats = np.array([grouped_stats[tc] for tc in true_counts])

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.35
    index = np.arange(len(true_counts))

    ax.bar(index, win_stats[:, 0], bar_width, label='Loss', color='red')
    ax.bar(index, win_stats[:, 1], bar_width, bottom=win_stats[:, 0], label='Draw', color='blue')
    ax.bar(index, win_stats[:, 2], bar_width, bottom=win_stats[:, 0] + win_stats[:, 1], label='Win', color='green')

    ax.set_xlabel('True Count')
    ax.set_ylabel('Frequency')
    ax.set_title('Win Stats Grouped by True Count')
    ax.set_xticks(index)
    ax.set_xticklabels(true_counts)
    ax.legend()

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # plot_simulation_together()
    plot_win_data()
