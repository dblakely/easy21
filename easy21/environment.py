"""Problem 1: Implementation of Easy21 environment
"""
import random
from typing import Tuple, Union


def sample_card() -> int:
    value = random.choice(list(range(1, 11)))
    color = random.choices(["red", "black"], weights=[1 / 3, 2 / 3])

    return -1 * value if color[0] == "red" else value


def dealers_turn(dealer_sum: int, demo: bool = False):
    while True:
        if dealer_sum < 1 or dealer_sum >= 17:
            break

        card = sample_card()
        dealer_sum += card
        if demo:
            print(f"Dealer drew a {card} --> Dealer sum = {dealer_sum}")

    return dealer_sum


def get_start_state() -> Tuple[int]:
    # Just get abs value for the start state because they have to be black (ie positve) cards
    return abs(sample_card()), abs(sample_card())


def step(dealer_sum: int, player_sum: int, action: int, demo: bool = False) -> Tuple[Union[int, float]]:
    """Samples the environment and returns a new state given the current state and an action.
    Note that the dealer's moves are modeled as just being part of the environment.

    Parameters
    ----------
    state : State
        The current state
    action : int
        Action taken, either "hit" or "stick".
        Calling step with a stick action will play out the dealer's cards and return the final reward and terminal state.

    Returns
    -------
    Tuple[State, float]
        The next state and the reward
    """
    reward = None

    # Hit - player draws another card
    if action == 0:
        # Return a new card to the agent
        next_card = sample_card()
        player_sum += next_card
        if demo:
            print(f"Player drew a {next_card} --> Player sum = {player_sum}")

        if player_sum < 1 or player_sum > 21:
            # Player went bust
            reward = -1
    # Stick - the dealer will repeatedly draw cards
    else:
        dealer_sum = dealers_turn(dealer_sum, demo=demo)

        if dealer_sum < 1 or dealer_sum > 21 or player_sum > dealer_sum:
            reward = 1
        elif dealer_sum == player_sum:
            reward = 0
        elif dealer_sum > player_sum:
            reward = -1

    return dealer_sum, player_sum, reward
