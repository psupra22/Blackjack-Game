import random
from typing import List
from collections.abc import Callable

class Deck:
    """
    Represents a 52-card deck with shuffle and deal functionality
    """
    def __init__(self) -> None:
        self.reset()


    def reset(self) -> None:
        """
        Inititalize and shuffle deck
        """
        suits: List[str] = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks: List[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self._cards: List[tuple[str, str]] = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self._cards)


    def deal(self) -> tuple[str, str]:
        """
        Deal card; reshuffle if empty
        """
        if not self._cards:
            self.reset()

        return self._cards.pop()


class BlackJackGame:
    """
    Manages game state, player state, dealer logic and bankroll
    """
    def __init__(self, deck: Deck, bankroll: int,
                 input_func: Callable[[str], str] = input) -> None:
        self.deck: Deck = deck
        self.bankroll: int = bankroll
        self.input: Callable[[str], str] = input_func
        self.player_hand: List[tuple[str, str]] = []
        self.dealer_hand: List[tuple[str, str]] = []


    def initial_deal(self) -> None:
        """
        Deal two cards to player and dealer to start round
        """
        self.player_hand: List[tuple[str, str]] = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand: List[tuple[str, str]] = [self.deck.deal(), self.deck.deal()]


    def get_score(self, hand: List[tuple[str, str]]) -> int:
        """
        Calculates optimal Blackjack score for a hand
        """
        total: int = 0
        aces: int = 0

        for rank, _ in hand:
            if rank in ["J", "Q", "K"]:
                total += 10
            elif rank == "A":
                aces += 1
            else:
                total += int(rank)

        # Add aces optimally
        for _ in range(aces):
            # Prefer 11 if not bust
            if (total + 11) <= 21:
                total += 11
            else:
                total += 1

        return total


    def place_bet(self) -> int:
        """
        Prompts player for a bet, validating against bankroll
        """
        while True:
            try:
                bet: int = int(input(f"Bankroll: ${self.bankroll}. Enter bet: "))
                if 1 <= bet <= self.bankroll:
                    return bet

                print("Bet must be positive and no more than your bankroll.")
            except ValueError:
                print("Please enter a valid integer.")


    def player_turn(self) -> None:
        """
        Manages player hit/stand until the bust
        """
        while True:
            score: int = self.get_score(self.player_hand)
            print(f"Your hand: {self.player_hand} (score: {score})")
            if score > 21:
                print("You busted")
                return

            action: str = self.input("Hit or stand? (h/s): ").strip().lower()
            if action == 'h':
                self.player_hand.append(self.deck.deal())
            elif action == 's':
                break
            else:
                print("Invalid choice; enter 'h' or 's'.")


    def dealer_turn(self) -> None:
        """
        Dealer draws until reaching at least 17.
        """
        while self.get_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.deal())


    def settle_bets(self, bet: int) -> None:
        """
        Compares hands, adjusts bankroll, and prints outcome messages.
        """
        player_score: int = self.get_score(self.player_hand)
        dealer_score: int = self.get_score(self.dealer_hand)
        print(f"Dealer hand: {self.dealer_hand} (score: {dealer_score})")

        # Natural blackjack
        if player_score == 21 and len(self.player_hand) == 2:
            payout = int(1.5 * bet)
            print("Blackjack! You win 3:2 payout.")
            self.bankroll += payout
        elif player_score > 21:
            # Already busted in player_turn
            self.bankroll -= bet
        elif dealer_score > 21 or player_score > dealer_score:
            print("You win!")
            self.bankroll += bet
        elif player_score == dealer_score:
            print("Push. Bet returned.")
        else:
            print("Dealer wins.")
            self.bankroll -= bet


    def play_round(self) -> None:
        """
        Executes one full round of Blackjack, including betting and turns.
        """
        bet: int = self.place_bet()
        self.initial_deal()
        print(f"Dealer shows: {self.dealer_hand[0]}")

        # Check for player natural
        if self.get_score(self.player_hand) == 21:
            print("Blackjack!")
            self.settle_bets(bet)
            return

        self.player_turn()
        if self.get_score(self.player_hand) <= 21:
            self.dealer_turn()
        self.settle_bets(bet)
