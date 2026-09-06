"""Manual sanity checks for flor/pieza rules, hand-computed against the spec.

Truco Uruguayo flor ("flower") rules (see Hand.has_flower docstring):
  1. Three cards of the same suit.
  2. One pieza and two (non-pieza) cards of the same suit.
  3. Two piezas.
  4. Three piezas.

Pieza rules (see Card.is_pieza docstring): a card matches the muestra's suit
and its rank is one of {2, 4, 5, 10, 11}, or it is the 12 of the muestra's
suit when the muestra's own rank is one of {2, 4, 5, 10, 11}.
"""

from truco.domain.card import Card, Rank, Suit
from truco.domain.hand import Hand

MUESTRA = Card(Suit.ESPADA, Rank.THREE)


def test_three_cards_same_suit_is_flower() -> None:
    hand = Hand(
        [
            Card(Suit.ORO, Rank.ONE),
            Card(Suit.ORO, Rank.THREE),
            Card(Suit.ORO, Rank.SIX),
        ]
    )
    assert hand.has_flower(MUESTRA) is True


def test_three_different_suits_no_piezas_is_not_flower() -> None:
    hand = Hand(
        [
            Card(Suit.ORO, Rank.ONE),
            Card(Suit.COPA, Rank.THREE),
            Card(Suit.BASTO, Rank.SIX),
        ]
    )
    assert hand.has_flower(MUESTRA) is False


def test_one_pieza_plus_two_same_suit_is_flower() -> None:
    # Card(ESPADA, FOUR) is a pieza against MUESTRA (ESPADA THREE).
    hand = Hand(
        [
            Card(Suit.ESPADA, Rank.FOUR),
            Card(Suit.ORO, Rank.ONE),
            Card(Suit.ORO, Rank.SIX),
        ]
    )
    assert hand.has_flower(MUESTRA) is True


def test_one_pieza_plus_two_different_suits_is_not_flower() -> None:
    hand = Hand(
        [
            Card(Suit.ESPADA, Rank.FOUR),
            Card(Suit.ORO, Rank.ONE),
            Card(Suit.COPA, Rank.SIX),
        ]
    )
    assert hand.has_flower(MUESTRA) is False


def test_two_piezas_is_flower() -> None:
    hand = Hand(
        [
            Card(Suit.ESPADA, Rank.FOUR),
            Card(Suit.ESPADA, Rank.FIVE),
            Card(Suit.ORO, Rank.SIX),
        ]
    )
    assert hand.has_flower(MUESTRA) is True


def test_pieza_matches_muestra_suit_and_rank() -> None:
    assert Card(Suit.ESPADA, Rank.FOUR).is_pieza(MUESTRA) is True


def test_non_pieza_rank_same_suit_as_muestra() -> None:
    assert Card(Suit.ESPADA, Rank.ONE).is_pieza(MUESTRA) is False


def test_pieza_rank_different_suit_than_muestra() -> None:
    assert Card(Suit.ORO, Rank.FOUR).is_pieza(MUESTRA) is False


def test_twelve_is_pieza_when_muestra_rank_is_special() -> None:
    muestra = Card(Suit.COPA, Rank.FOUR)
    assert Card(Suit.COPA, Rank.TWELVE).is_pieza(muestra) is True


def test_twelve_is_not_pieza_when_muestra_rank_is_not_special() -> None:
    muestra = Card(Suit.COPA, Rank.THREE)
    assert Card(Suit.COPA, Rank.TWELVE).is_pieza(muestra) is False
