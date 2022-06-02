from argparse import ArgumentParser

import matplotlib.pyplot as plt
import numpy as np

from easy21 import QFunction, monte_carlo_control, td_control


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--max_episodes", default=1000, type=int)
    parser.add_argument("--algo", type=str, choices=["mc", "td"])
    parser.add_argument("--N0", type=int, default=100)
    parser.add_argument("--value_function_plot_name", type=str, default="value_function.pdf")
    return parser.parse_args()


def plot_value_function(Q: QFunction, plot_name: str) -> None:
    x = np.arange(0, 11)  # Dealer
    y = np.arange(0, 22)  # Player

    X, Y = np.meshgrid(x, y)
    Z = np.max(Q.table, axis=2)

    # fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, Z.transpose(), rstride=1, cstride=1, cmap="viridis")

    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    ax.set_zlabel("V*")
    ax.set_title("Easy21 Monte Carlo Control")

    plt.show()


def main(args):
    if args.algo == "mc":
        Q: QFunction = monte_carlo_control(args.max_episodes, args.N0)
        plot_value_function(Q, args.value_function_plot_name)
    elif args.algo == "td":
        Q: QFunction = td_control(args.max_episodes)


if __name__ == "__main__":
    args = get_args()
    main(args)
