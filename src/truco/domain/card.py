from enum import Enum, auto


class Suit(Enum):
    ORO = auto()
    COPA = auto()
    ESPADA = auto()
    BASTO = auto()


class Rank(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    TEN = 10
    ELEVEN = 11
    TWELVE = 12


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def is_pieza(self, muestra: "Card") -> bool:
        """
        Check if this card is a 'pieza' based on the muestra.

        Args:
            muestra: The trump card for this hand

        Returns:
            True if the card is a pieza, False otherwise
        """
        if self.suit != muestra.suit:
            return False

        if self.rank in [Rank.TWO, Rank.FOUR, Rank.FIVE, Rank.TEN, Rank.ELEVEN]:
            return True

        if self.rank == Rank.TWELVE and muestra.rank in [
            Rank.TWO,
            Rank.FOUR,
            Rank.FIVE,
            Rank.TEN,
            Rank.ELEVEN,
        ]:
            return True

        return False

    def __str__(self) -> str:
        return f"{self.rank.name} of {self.suit.name}"

    def __repr__(self) -> str:
        return f"Card({self.suit.name}, {self.rank.name})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self) -> int:
        return hash((self.suit, self.rank))
