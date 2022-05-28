from easy21 import environment


def play_game():
    dealer_sum, player_sum = environment.get_start_state()
    print(f"Dealer sum: {dealer_sum}")
    print(f"Player sum: {player_sum}")

    while True:
        action = input("Hit or stick? ")
        if action == "h" or action == "hit":
            action = 0
        else:
            action = 1

        dealer_sum, player_sum, reward = environment.step(dealer_sum, player_sum, action, demo=True)

        if action == "hit":
            if reward == -1:
                print(f"Bust: {player_sum}")
        else:
            if reward == -1:
                print(f"Dealer wins: dealer has {dealer_sum} vs player's {player_sum}")
            elif reward == 0:
                print(f"Draw: dealer has {dealer_sum} vs player's {player_sum}")
            elif reward == 1:
                print(f"Dealer went bust: dealer has {dealer_sum} vs player's {player_sum}")

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
