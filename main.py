# Goal - have a hand higher than dealer but not over 21
# Bust - hand higher than 21
# Cards 2-10 are scored face value
# J, K, Q are all scored as 10
# A is scored either 1 or 11(you choose which)

# Starts by players placing a bet
# Dealer deals everyone a card faced up including himself
# Dealer deals everyone another card faced up, including himself but faced down
# If your score is 21 total you win 1.5x and you're done for that round
# Otherwise dealer asks if you want another card(if so hit else stay).
# There is no limit on hits but if you bust, dealer takes your bet
# Once everyone choose what they want to do, the dealer flips over his card
# If dealer has 16 or lower, they take another card
# If dealer has 17 or higher, they have to stay with their hand
# If the dealer busts, everyone still in the round wins 2x their bet
# If the dealer doesn't bust, only the player with a hand higher than dealer win 2x their bet and everyone else loses
# Then a new round begins

import shutil
from black_jack import Deck, BlackJackGame

def main() -> None:
    bankroll: int = get_bankroll()
    deck: Deck = Deck()
    game: BlackJackGame = BlackJackGame(deck, bankroll)

    while game.bankroll > 0:
        game.play_round()
        cont: str = input("Play another round? (y/n): ").strip().lower()
        if cont != 'y':
            break

        clear_screen()

    print(f"Game over! Final bankroll: ${game.bankroll}")


def get_bankroll() -> int:
    while True:
        try:
            bankroll: int = int(input("Enter bankroll: "))
            if bankroll <= 0:
                raise ValueError("Bankroll must be a integer greater than 0.")
            
            return bankroll
        except ValueError as message:
            print(message)


def clear_screen() -> None:
    columns: int = shutil.get_terminal_size().columns
    print("\n" * columns)


if __name__ == "__main__":
    main()
