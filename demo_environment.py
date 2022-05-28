from easy21 import environment


def play_game():
    state = environment.get_start_state()
    print(f"Dealer sum: {state.dealer_sum}")
    print(f"Player sum: {state.player_sum}")

    while True:
        action = input("Hit or stick? ")
        if action == "h":
            action = "hit"

        state, reward = environment.step(state, action, demo=True)

        if action == "hit":
            if reward == -1 and action == "hit":
                print(f"Bust: {state.player_sum}")
        else:
            if reward == -1:
                print(f"Dealer wins: dealer has {state.dealer_sum} vs player's {state.player_sum}")
            elif reward == 0:
                print(f"Draw: dealer has {state.dealer_sum} vs player's {state.player_sum}")
            elif reward == 1:
                print(f"Dealer went bust: dealer has {state.dealer_sum} vs player's {state.player_sum}")

        print("-" * 50)

        if reward is not None:
            break


def main():
    while True:
        play_game()
        play_again = input("Play again? (y/n) ")
        if play_again not in ["y", "Y", "yes"]:
            break


if __name__ == "__main__":
    main()
