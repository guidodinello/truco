import random
from typing import List, Optional

from truco.domain.card import Card, Rank, Suit


class Deck:
    def __init__(self):
        self.cards = self._create_standard_deck()
        self.shuffled = False
        self.muestra = None

    @staticmethod
    def _create_standard_deck() -> List[Card]:
        """Create a standard 40-card Spanish deck used in Truco Uruguayo."""
        cards = []
        for suit in Suit:
            for rank in Rank:
                cards.append(Card(suit, rank))
        return cards

    def shuffle(self, seed: Optional[int] = None) -> None:
        """
        Shuffle the deck.

        Args:
            seed: Optional random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        self.shuffled = True

    def deal(self, count: int) -> List[Card]:
        """
        Deal a specified number of cards from the deck.

        Args:
            count: Number of cards to deal

        Returns:
            List of dealt cards
        """
        if count > len(self.cards):
            raise ValueError(
                f"Cannot deal {count} cards. Only {len(self.cards)} left in deck."
            )

        dealt_cards = self.cards[:count]
        self.cards = self.cards[count:]

        return dealt_cards

    def reset(self) -> None:
        """Reset the deck to its initial state."""
        self.cards = self._create_standard_deck()
        self.shuffled = False
        self.muestra = None

    def __len__(self) -> int:
        return len(self.cards)
