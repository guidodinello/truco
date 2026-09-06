from typing import List

from truco.domain.card import Card
from truco.domain.player import Player


class Team:
    def __init__(self, team_id: int, name: str = None):
        self.id = team_id
        self.name = name or f"Team {team_id}"
        self.players: List[Player] = []

    def add_player(self, player: Player) -> None:
        player.set_team(self.id)
        self.players.append(player)

    def get_players_with_flower(self, muestra: Card = None) -> List[Player]:
        """
        Get all players in the team who have a flower.

        Args:
            muestra: The trump card for this hand

        Returns:
            List of players who have a flower
        """
        return [player for player in self.players if player.has_flower(muestra)]

    def has_players_with_flower(self, count: int, muestra: Card = None) -> bool:
        """
        Check if at least 'count' players in the team have a flower.

        Args:
            count: Minimum number of players with flower
            muestra: The trump card for this hand

        Returns:
            True if at least 'count' players have a flower, False otherwise
        """
        flower_count = len(self.get_players_with_flower(muestra))
        return flower_count >= count

    def get_players_with_pieza(self, muestra: Card) -> List[Player]:
        """
        Get all players in the team who have at least one pieza.

        Args:
            muestra: The trump card for this hand

        Returns:
            List of players who have at least one pieza
        """
        return [player for player in self.players if player.has_pieza(muestra)]

    def has_players_with_pieza(self, count: int, muestra: Card) -> bool:
        """
        Check if at least 'count' players in the team have a pieza.

        Args:
            count: Minimum number of players with pieza
            muestra: The trump card for this hand

        Returns:
            True if at least 'count' players have a pieza, False otherwise
        """
        pieza_count = len(self.get_players_with_pieza(muestra))
        return pieza_count >= count

    def __len__(self) -> int:
        return len(self.players)

    def __str__(self) -> str:
        return f"{self.name} ({len(self.players)} players)"
