from typing import Dict, List, Optional

from truco.domain.deck import Deck
from truco.domain.player import Player
from truco.domain.team import Team


class Game:
    def __init__(self, num_players_per_team: int = 3, num_teams: int = 2):
        self.num_players_per_team = num_players_per_team
        self.num_teams = num_teams
        self.teams: List[Team] = []
        self.players: List[Player] = []
        self.deck = Deck()
        self.muestra = None

        self._setup_teams_and_players()

    def _setup_teams_and_players(self) -> None:
        total_players = self.num_teams * self.num_players_per_team

        for i in range(self.num_teams):
            self.teams.append(Team(i))

        for i in range(total_players):
            player = Player(i)
            team_id = i % self.num_teams
            self.teams[team_id].add_player(player)
            self.players.append(player)

    def deal_cards(self, seed: Optional[int] = None) -> None:
        """
        Deal cards to all players and determine the muestra card.

        In Truco Uruguayo, after dealing to all players, the next card is turned face up
        and becomes the "muestra" (trump card).

        Args:
            seed: Optional random seed for reproducibility
        """
        # Reset the deck and shuffle
        self.deck.reset()
        self.deck.shuffle(seed)

        # Clear any existing cards from player hands
        for player in self.players:
            player.hand.cards.clear()

        # Deal 3 cards to each player
        for player in self.players:
            cards = self.deck.deal(3)
            player.hand.add_cards(cards)

        # Draw the muestra card
        self.muestra = self.deck.deal(1)[0]

    def count_players_with_flower(self) -> int:
        """Count how many players have a flower considering the muestra."""
        return sum(1 for player in self.players if player.has_flower(self.muestra))

    def get_flower_distribution(self) -> Dict[int, int]:
        """
        Get the distribution of flowers among teams.

        Returns:
            Dictionary mapping team_id to the number of players with flower in that team
        """
        return {
            team.id: len(team.get_players_with_flower(self.muestra))
            for team in self.teams
        }

    def is_all_flowers_in_same_team(self) -> bool:
        """
        Check if all players with flowers are in the same team.

        Returns:
            True if all players with flowers are in the same team, False otherwise
        """
        flowers_by_team = self.get_flower_distribution()
        players_with_flower = self.count_players_with_flower()

        # If no players have flowers, return False
        if players_with_flower == 0:
            return False

        # Check if any team has all the flowers
        return any(count == players_with_flower for count in flowers_by_team.values())

    def count_players_with_piezas(self) -> int:
        """Count how many players have at least one pieza."""
        return sum(1 for player in self.players if player.has_pieza(self.muestra))

    def get_pieza_distribution(self) -> Dict[int, int]:
        """
        Get the distribution of players with piezas among teams.

        Returns:
            Dictionary mapping team_id to the number of players with piezas in that team
        """
        if not self.muestra:
            return {team.id: 0 for team in self.teams}

        return {
            team.id: len(team.get_players_with_pieza(self.muestra))
            for team in self.teams
        }
