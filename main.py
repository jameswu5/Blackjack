import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from game import Game

seed = 42


def plot_card_counter(runs=1):
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.title('Player Bankroll')
    plt.xlabel('Round')
    plt.ylabel('Bankroll')

    plt.subplot(2, 1, 2)
    plt.title('True Count')
    plt.axhline(0, linestyle='--')
    plt.xlabel('Round')
    plt.ylabel('True Count')

    for i in range(runs):
        cur_seed = seed + i if seed else None
        player_type = "counter"
        g = Game(player_type=player_type, seed=cur_seed)
        g.simulate(1000)

        plt.subplot(2, 1, 1)
        plt.plot(g.player_bankroll)

        plt.subplot(2, 1, 2)
        plt.plot(g.true_count)
        if runs == 1:
            for j in g.new_shoes:
                plt.axvline(j, color='grey', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()


def plot_final_bankroll_histogram(runs=1000, rounds=1000):
    final_bankrolls_basic = []
    final_bankrolls_counter = []
    for i in range(runs):
        cur_seed = seed + i if seed else None
        g = Game(player_type="basic", seed=cur_seed)
        g.simulate(rounds)
        final_bankrolls_basic.append(g.player_bankroll[-1])

        g2 = Game(player_type="counter", seed=cur_seed)
        g2.simulate(rounds)
        final_bankrolls_counter.append(g2.player_bankroll[-1])

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.hist(final_bankrolls_basic, bins=50, edgecolor='black')
    plt.axvline(np.mean(final_bankrolls_basic), color='red', linestyle='--', label='Mean')
    plt.title('Basic Strategy')
    plt.xlabel('Final Bankroll')
    plt.ylabel('Frequency')

    plt.subplot(2, 1, 2)
    plt.hist(final_bankrolls_counter, bins=50, edgecolor='black')
    plt.axvline(np.mean(final_bankrolls_counter), color='red', linestyle='--', label='Mean')
    plt.title('Card Counter')
    plt.xlabel('Final Bankroll')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()


def plot_win_data():
    player_type = "counter"
    g = Game(player_type=player_type, seed=seed)
    g.simulate(100000)

    grouped_stats = defaultdict(lambda: [0, 0, 0])
    for tc, ws in zip(g.true_count, g.win_stats):
        grouped_stats[tc][int(ws)+1] += 1

    true_counts = sorted(grouped_stats.keys())
    win_stats = np.array([grouped_stats[tc] for tc in true_counts])
    win_stats_percent = win_stats / win_stats.sum(axis=1, keepdims=True) * 100

    bar_width = 0.35
    index = np.arange(len(true_counts))

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.bar(index, win_stats[:, 0], bar_width, label='Loss', color='red')
    plt.bar(index, win_stats[:, 1], bar_width, bottom=win_stats[:, 0], label='Draw', color='blue')
    plt.bar(index, win_stats[:, 2], bar_width, bottom=win_stats[:, 0] + win_stats[:, 1], label='Win', color='green')
    plt.ylabel('Frequency')
    plt.title('Win Stats Grouped by True Count')
    plt.xticks(index, true_counts)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.bar(index, win_stats_percent[:, 0], bar_width, label='Loss', color='red')
    plt.bar(index, win_stats_percent[:, 1], bar_width, bottom=win_stats_percent[:, 0], label='Draw', color='blue')
    plt.bar(index, win_stats_percent[:, 2], bar_width, bottom=win_stats_percent[:, 0] + win_stats_percent[:, 1], label='Win', color='green')
    plt.xlabel('True Count')
    plt.ylabel('Percentage')
    plt.xticks(index, true_counts)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_card_counter(1)
    # plot_win_data()
    # plot_final_bankroll_histogram()
