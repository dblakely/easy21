import unittest

from easy21 import QFunction, State, monte_carlo_update_from_episode


class TestMonteCarloUpdate(unittest.TestCase):
    def test_update_from_episode_1(self):
        Q = QFunction()
        state_action_counts = {}

        episode = [
            (State(10, 5), "hit"),
            (State(10, 10), "hit"),
            (State(10, 20), "stick"),
        ]
        reward = 1

        Q, state_action_counts = monte_carlo_update_from_episode(
            episode=episode, reward=reward, Q=Q, state_action_counts=state_action_counts
        )

        expected_vals = [1, 1, 1]
        for i, state_action in enumerate(episode):
            self.assertEqual(Q(*state_action), expected_vals[i])

        episode = [
            (State(10, 4), "hit"),
            (State(10, 10), "hit"),
            (State(10, 20), "hit"),
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
