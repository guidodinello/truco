from truco.domain.card import Card
from truco.domain.hand import Hand


class Player:
    def __init__(self, player_id: int, name: str = None):
        self.id = player_id
        self.name = name or f"Player {player_id}"
        self.hand = Hand()
        self.team_id = None

    def set_team(self, team_id: int) -> None:
        self.team_id = team_id

    def has_flower(self, muestra: Card = None) -> bool:
        """
        Check if the player has a flower.

        Args:
            muestra: The trump card for this hand

        Returns:
            True if the player has a flower, False otherwise
        """
        return self.hand.has_flower(muestra)

    def has_pieza(self, muestra: Card) -> bool:
        """
        Check if the player has any pieza cards.

        Args:
            muestra: The trump card for this hand

        Returns:
            True if the player has at least one pieza, False otherwise
        """
        return self.hand.has_pieza(muestra)

    def __str__(self) -> str:
        return f"{self.name} (Team {self.team_id})"

    def __repr__(self) -> str:
        return f"Player(id={self.id}, name={self.name}, team={self.team_id})"
