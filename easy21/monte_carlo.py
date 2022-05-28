from typing import Dict, List, Optional, Tuple

import numpy as np
from tqdm import tqdm

from .environment import State, get_start_state, step


class QFunction:
    def __init__(self):
        # 10 dealer states, 21 player states, 2 actions
        # We'll say action idx 0 = hit, action idx 1 = stick
        self.table = np.zeros((10, 21, 2))

    def __call__(self, state: State, action: Optional[str]) -> float:
        dealer = state.dealer_sum
        player = state.player_sum

        # If no action provided, treat this as a call to the value function
        if action is None:
            return np.argmax(self.table[dealer - 1, player - 1, :])

        action_idx = int(action == "stick")
        return self.table[dealer - 1, player - 1, action_idx]

    def greedy_action(self, state: State):
        dealer = state.dealer_sum
        player = state.player_sum
        action_values = self.table[dealer - 1, player - 1, :]

        # Tie-breaking
        if action_values[0] == action_values[1]:
            action = np.random.choice([0, 1])
        else:
            action = np.argmax(self.table[dealer - 1, player - 1, :])

        return "hit" if action == 0 else "stick"

    def sample_policy(self, state: State, state_action_counts: Dict):
        greedy_action = self.greedy_action(state)

        num_visits = state_action_counts.get((state, "hit"), 1) + state_action_counts.get((state, "stick"), 1)
        epsilon = 100 / (100 + num_visits)

        coin_toss = np.random.uniform()
        if coin_toss < 1 - epsilon + (epsilon / 2):
            return greedy_action

        return "hit" if greedy_action == "stick" else "stick"

    def update_value(self, state: State, action: str, update: float):
        dealer = state.dealer_sum
        player = state.player_sum
        action_idx = int(action == "stick")

        self.table[dealer - 1, player - 1, action_idx] += update


def generate_episode(Q: QFunction, state_action_counts: Dict) -> Tuple[List[State], float]:
    reward = None
    state = get_start_state()
    episode = []

    # Episode is over when a reward is returned by the environment
    while reward is None:
        action = Q.sample_policy(state, state_action_counts)
        episode.append((state, action))

        state, reward = step(state, action)

        if reward is not None:
            break

    return episode, reward


# def monte_carlo_episode_update(episode: List[Tuple[State, str]], Q: QFunction) -> QFunction:
def monte_carlo_update_from_episode(
    episode: List[Tuple[State, str]], reward: float, Q: QFunction, state_action_counts: Dict
) -> Tuple[QFunction, np.ndarray]:
    for i in range(len(episode) - 1, -1, -1):
        state, action = episode[i]

        # Update state-action counts
        if (state, action) not in state_action_counts:
            state_action_counts[(state, action)] = 1
        else:
            state_action_counts[(state, action)] += 1

        # State-action value
        update = (reward - Q(state, action)) / state_action_counts[(state, action)]
        Q.update_value(state, action, update)

    return Q, state_action_counts


def monte_carlo_control(max_iters: int = 100):
    Q = QFunction()
    iters = 0

    state_action_counts = {}

    progress_bar = tqdm(total=max_iters)
    while iters < max_iters:
        episode, reward = generate_episode(Q, state_action_counts)
        Q, state_action_counts = monte_carlo_update_from_episode(
            episode=episode, reward=reward, Q=Q, state_action_counts=state_action_counts
        )
        iters += 1
        progress_bar.update(1)

    return Q
