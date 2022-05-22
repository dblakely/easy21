import random
import unittest

from easy21 import dealers_turn, get_start_state, sample_card

random.seed(0)


class TestEnvironment(unittest.TestCase):
    def test_dealers_turn_sum_17(self):
        dealer_sum = dealers_turn(17)

        # Dealer will always hit if < 17 and always stick > 17
        self.assertEqual(dealer_sum, 17)

    def test_dealers_turn_sum_1(self):
        dealer_sum = dealers_turn(1)

        # Dealer will always hit if < 17 and always stick > 17
        self.assertGreaterEqual(dealer_sum, 17)

    def test_dealers_turn_sum_negative_1(self):
        dealer_sum = dealers_turn(-1)

        # Dealer will always hit if < 17 and always stick > 17
        self.assertLessEqual(dealer_sum, -1)

    def test_sample_card(self):
        for _ in range(50):
            card = sample_card()
            self.assertTrue(abs(card) in list(range(1, 11)))

    def test_get_start_state(self):
        for _ in range(50):
            state = get_start_state()
            self.assertTrue(state.dealer_sum >= 1)
            self.assertTrue(state.player_sum >= 1)


if __name__ == "__main__":
    unittest.main()
