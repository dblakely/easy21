import unittest

import numpy as np

from easy21 import QFunction, monte_carlo_update_from_episode


class TestMonteCarloUpdate(unittest.TestCase):
    def test_update_from_episode_1(self):
        Q = QFunction()
        state_action_counts = np.zeros((11, 22, 2))

        episode = [
            (10, 5, 0),
            (10, 10, 0),
            (10, 20, 1),
        ]
        reward = 1

        Q, state_action_counts = monte_carlo_update_from_episode(
            episode=episode, reward=reward, Q=Q, state_action_counts=state_action_counts
        )

        expected_vals = [1, 1, 1]
        for i, state_action in enumerate(episode):
            self.assertEqual(Q(*state_action), expected_vals[i])

        episode = [
            (10, 4, 0),
            (10, 10, 0),
            (10, 20, 0),
        ]
        reward = -1

        Q, state_action_counts = monte_carlo_update_from_episode(
            episode=episode, reward=reward, Q=Q, state_action_counts=state_action_counts
        )

        expected_vals = [-1, 0, -1]
        for i, state_action in enumerate(episode):
            self.assertEqual(Q(*state_action), expected_vals[i])


if __name__ == "__main__":
    unittest.main()
