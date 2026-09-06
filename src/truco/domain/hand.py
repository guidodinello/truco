from typing import List, Optional

from truco.domain.card import Card, Suit


class Hand:
    def __init__(self, cards: Optional[List[Card]] = None):
        self.cards = cards or []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def add_cards(self, cards: List[Card]) -> None:
        self.cards.extend(cards)

    def has_flower(self, muestra: Optional[Card] = None) -> bool:
        """
        Check if the hand has a flower.

        In Truco Uruguayo, a flower ("flor") can be:
        1. Three cards of the same suit
        2. One pieza and two cards of the same suit
        3. Two piezas
        4. Three piezas

        Args:
            muestra: The trump card for this hand (required for checking piezas)

        Returns:
            True if the hand has a flower, False otherwise
        """
        # Case 1: Three cards of the same suit
        suit_counts = {suit: 0 for suit in Suit}
        for card in self.cards:
            suit_counts[card.suit] += 1

        if any(count == 3 for count in suit_counts.values()):
            return True

        # Can't check for piezas without muestra
        if not muestra:
            return False

        # Get piezas in the hand
        piezas = [card for card in self.cards if card.is_pieza(muestra)]
        num_piezas = len(piezas)

        # Case 3 and 4: Two or three piezas
        if num_piezas >= 2:
            return True

        # Case 2: One pieza and two cards of the same suit
        if num_piezas == 1:
            pieza = piezas[0]
            # Count cards of each suit excluding the pieza
            suit_counts_no_pieza = {suit: 0 for suit in Suit}
            for card in self.cards:
                if card != pieza:
                    suit_counts_no_pieza[card.suit] += 1

            # Check if any suit has at least 2 cards
            if any(count >= 2 for count in suit_counts_no_pieza.values()):
                return True

        return False

    def has_pieza(self, muestra: Card) -> bool:
        """
        Check if the hand has any pieza cards.

        Args:
            muestra: The trump card for this hand

        Returns:
            True if the hand has at least one pieza, False otherwise
        """
        return any(card.is_pieza(muestra) for card in self.cards)

    def get_piezas(self, muestra: Card) -> List[Card]:
        """
        Get all pieza cards in the hand.

        Args:
            muestra: The trump card for this hand

        Returns:
            List of pieza cards in the hand
        """
        return [card for card in self.cards if card.is_pieza(muestra)]

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return str(self.cards)
