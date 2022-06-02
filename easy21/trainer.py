import numpy as np


class Trainer:
    def __init__(self, max_episodes: int = 1000, N0: int = 100):
        self.max_epispdes = max_episodes
        self.N0 = N0

        # 10 dealer states, 21 player states, 2 actions
        # We'll say action idx 0 = hit, action idx 1 = stick
        self.Q = np.zeros((11, 22, 2))
        self.state_action_counts = np.zeros((11, 22, 2))

    def train(self):
        pass
