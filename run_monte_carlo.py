from argparse import ArgumentParser

import matplotlib.pyplot as plt
import numpy as np

from easy21 import QFunction, monte_carlo_control


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--max_iters", default=100, type=int)
    parser.add_argument("--algorithm", type=str, choices=["monte_carlo"])
    parser.add_argument("--value_function_plot_name", type=str, default="value_function.pdf")
    return parser.parse_args()


def plot_value_function(Q: QFunction, plot_name: str) -> None:
    x = np.arange(0, 10)  # Dealer
    y = np.arange(0, 21)  # Player

    X, Y = np.meshgrid(x, y)
    Z = np.max(Q.table, axis=2)

    # fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_wireframe(X, Y, Z.transpose(), rstride=1, cstride=1, color="black")

    ax.set_xlabel("Dealer Showing")
    ax.set_ylabel("Player Sum")
    ax.set_zlabel("V*")

    plt.show()


def main(args):
    Q: QFunction = monte_carlo_control(args.max_iters)
    plot_value_function(Q, args.value_function_plot_name)


if __name__ == "__main__":
    args = get_args()
    main(args)
