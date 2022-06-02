from typing import List, Optional, Tuple

import numpy as np
from tqdm import tqdm

from .environment import get_start_state, step


class QFunction:
    def __init__(self, N0: int = 100):
        # 10 dealer states, 21 player states, 2 actions
        # We'll say action idx 0 = hit, action idx 1 = stick
        self.table = np.zeros((11, 22, 2))
        self.N0 = N0

    def __call__(self, dealer_sum: int, player_sum: int, action: Optional[int] = None) -> float:
        # If no action provided, treat this as a call to the value function
        if action is None:
            return np.argmax(self.table[dealer_sum, player_sum, :])

        return self.table[dealer_sum, player_sum, action]

    def greedy_action(self, dealer_sum: int, player_sum: int):
        action_values = self.table[dealer_sum, player_sum, :]

        # Tie-breaking
        if action_values[0] == action_values[1]:
            action = np.random.choice([0, 1])
        else:
            action = np.argmax(self.table[dealer_sum, dealer_sum])

        return action

    def sample_policy(self, dealer_sum: int, player_sum: int, state_action_counts: np.ndarray):
        greedy_action = self.greedy_action(dealer_sum, player_sum)

        epsilon = self.N0 / (self.N0 + np.sum(state_action_counts[dealer_sum, player_sum]))

        coin_toss = np.random.uniform()
        if coin_toss < 1 - epsilon + (epsilon / 2):
            return greedy_action

        return 1 if greedy_action == 0 else 0

    def update_value(self, dealer_sum, player_sum, action: int, update: float):
        self.table[dealer_sum, player_sum, action] += update


def generate_episode(Q: QFunction, state_action_counts: np.ndarray):
    reward = None
    dealer_sum, player_sum = get_start_state()
    episode = []

    # Episode is over when a reward is returned by the environment
    while reward is None:
        action = Q.sample_policy(dealer_sum, player_sum, state_action_counts)
        episode.append((dealer_sum, player_sum, action))

        dealer_sum, player_sum, reward = step(dealer_sum, player_sum, action)

        if reward is not None:
            break

    return episode, reward


def monte_carlo_update_from_episode(
    episode: List[Tuple[int]], reward: float, Q: QFunction, state_action_counts: np.ndarray
) -> Tuple[QFunction, np.ndarray]:
    for i in range(len(episode) - 1, -1, -1):
        state_action = episode[i]
        state_action_counts[state_action] += 1

        # State-action value
        learning_rate = 1 / state_action_counts[state_action]
        update = learning_rate * (reward - Q(*state_action))
        Q.update_value(*state_action, update)

    return Q, state_action_counts


def monte_carlo_control(max_episodes: int = 1000, N0: int = 100):
    Q = QFunction(N0=N0)
    num_episodes = 0

    state_action_counts = np.zeros((11, 22, 2))

    progress_bar = tqdm(total=max_episodes)
    while num_episodes < max_episodes:
        episode, reward = generate_episode(Q, state_action_counts)
        Q, state_action_counts = monte_carlo_update_from_episode(
            episode=episode, reward=reward, Q=Q, state_action_counts=state_action_counts
        )
        num_episodes += 1
        progress_bar.update(1)

    return Q
