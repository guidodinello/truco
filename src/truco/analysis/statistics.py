"""Statistical analysis for Truco Uruguayo simulations."""

from typing import Any, Dict

import numpy as np

from truco.domain.card import Rank, Suit
from truco.simulation.simulator import SimulationResult


class StatisticsAnalyzer:
    """
    Provides statistical analysis for Truco simulations,
    with a focus on conditional probabilities and team distributions
    for both flowers and piezas.
    """

    def __init__(self, results: SimulationResult):
        self.results = results

    def calculate_probability_of_flower(self) -> Dict[int, float]:
        """
        Calculate the probability of different numbers of players having a flower.

        Returns:
            Dictionary mapping number of players to probability
        """
        total_games = self.results.total_games
        flower_counts = self.results.players_with_flower

        # Count occurrences of each number of players with flower
        counts = {}
        for i in range(max(flower_counts) + 1):
            counts[i] = flower_counts.count(i) / total_games

        return counts

    def calculate_probability_of_pieza(self) -> Dict[int, float]:
        """
        Calculate the probability of different numbers of players having a pieza.

        Returns:
            Dictionary mapping number of players to probability
        """
        total_games = self.results.total_games
        pieza_counts = self.results.players_with_pieza

        # Count occurrences of each number of players with pieza
        counts = {}
        for i in range(max(pieza_counts) + 1):
            counts[i] = pieza_counts.count(i) / total_games

        return counts

    def calculate_conditional_same_team_probability(self) -> Dict[str, float]:
        """
        Calculate conditional probabilities of flowers being in the same team.

        Returns:
            Dictionary with different conditional probabilities:
            - when_multiple_flowers: Probability all flowers are in same team, given multiple players have flowers
            - by_flower_count: Dict mapping flower count to probability all are in same team
        """
        flower_counts = self.results.players_with_flower
        same_team_flags = self.results.all_flowers_same_team

        # Initialize results
        result = {"when_multiple_flowers": 0.0, "by_flower_count": {}}

        # Count games with multiple flowers (2 or more)
        multi_flower_indices = [
            i for i, count in enumerate(flower_counts) if count >= 2
        ]

        if not multi_flower_indices:
            return result

        # Calculate probability when multiple flowers
        multi_flower_same_team = sum(
            1 for i in multi_flower_indices if same_team_flags[i]
        )
        result["when_multiple_flowers"] = multi_flower_same_team / len(
            multi_flower_indices
        )

        # Calculate probability by flower count
        max_flowers = max(flower_counts)
        for count in range(2, max_flowers + 1):
            count_indices = [i for i, fc in enumerate(flower_counts) if fc == count]

            if not count_indices:
                continue

            same_team_count = sum(1 for i in count_indices if same_team_flags[i])

            if len(count_indices) > 0:
                result["by_flower_count"][count] = same_team_count / len(count_indices)

        return result

    def calculate_conditional_same_team_pieza_probability(self) -> Dict[str, float]:
        """
        Calculate conditional probabilities of piezas being in the same team.

        Returns:
            Dictionary with different conditional probabilities:
            - when_multiple_piezas: Probability all piezas are in same team, given multiple players have piezas
            - by_pieza_count: Dict mapping pieza count to probability all are in same team
        """
        pieza_counts = self.results.players_with_pieza
        same_team_flags = self.results.all_piezas_same_team

        # Initialize results
        result = {"when_multiple_piezas": 0.0, "by_pieza_count": {}}

        # Count games with multiple piezas (2 or more)
        multi_pieza_indices = [i for i, count in enumerate(pieza_counts) if count >= 2]

        if not multi_pieza_indices:
            return result

        # Calculate probability when multiple piezas
        multi_pieza_same_team = sum(
            1 for i in multi_pieza_indices if same_team_flags[i]
        )
        result["when_multiple_piezas"] = multi_pieza_same_team / len(
            multi_pieza_indices
        )

        # Calculate probability by pieza count
        max_piezas = max(pieza_counts)
        for count in range(2, max_piezas + 1):
            count_indices = [i for i, pc in enumerate(pieza_counts) if pc == count]

            if not count_indices:
                continue

            same_team_count = sum(1 for i in count_indices if same_team_flags[i])

            if len(count_indices) > 0:
                result["by_pieza_count"][count] = same_team_count / len(count_indices)

        return result

    def calculate_team_advantage(self) -> Dict[str, Any]:
        """
        Calculate team advantage statistics based on flower distribution.

        Returns:
            Dictionary with team advantage statistics:
            - team_advantage_probability: Probability that one team has more flowers than the other
            - flower_distribution_by_advantage: Distribution of flower count differences between teams
        """
        result = {
            "team_advantage_probability": 0.0,
            "flower_distribution_by_advantage": {},
        }

        # Only proceed if we have at least one team distribution
        if not self.results.flower_distribution:
            return result

        # Get number of teams from first game
        num_teams = len(self.results.flower_distribution[0])

        # Skip if not a two-team game (current implementation only handles 2 teams)
        if num_teams != 2:
            return result

        advantages = []

        # Calculate flower count advantage for each game
        for game_distrib in self.results.flower_distribution:
            team0_flowers = game_distrib.get(0, 0)
            team1_flowers = game_distrib.get(1, 0)
            advantage = team0_flowers - team1_flowers
            advantages.append(advantage)

        # Calculate advantage distribution
        total_games = len(advantages)
        for adv in set(advantages):
            result["flower_distribution_by_advantage"][adv] = (
                advantages.count(adv) / total_games
            )

        # Calculate probability of team advantage (any non-zero advantage)
        team_advantage_count = sum(1 for adv in advantages if adv != 0)
        result["team_advantage_probability"] = team_advantage_count / total_games

        return result

    def calculate_pieza_team_advantage(self) -> Dict[str, Any]:
        """
        Calculate team advantage statistics based on pieza distribution.

        Returns:
            Dictionary with team advantage statistics:
            - team_advantage_probability: Probability that one team has more piezas than the other
            - pieza_distribution_by_advantage: Distribution of pieza count differences between teams
        """
        result = {
            "team_advantage_probability": 0.0,
            "pieza_distribution_by_advantage": {},
        }

        # Only proceed if we have at least one team distribution
        if not self.results.pieza_distribution:
            return result

        # Get number of teams from first game
        num_teams = len(self.results.pieza_distribution[0])

        # Skip if not a two-team game (current implementation only handles 2 teams)
        if num_teams != 2:
            return result

        advantages = []

        # Calculate pieza count advantage for each game
        for game_distrib in self.results.pieza_distribution:
            team0_piezas = game_distrib.get(0, 0)
            team1_piezas = game_distrib.get(1, 0)
            advantage = team0_piezas - team1_piezas
            advantages.append(advantage)

        # Calculate advantage distribution
        total_games = len(advantages)
        for adv in set(advantages):
            result["pieza_distribution_by_advantage"][adv] = (
                advantages.count(adv) / total_games
            )

        # Calculate probability of team advantage (any non-zero advantage)
        team_advantage_count = sum(1 for adv in advantages if adv != 0)
        result["team_advantage_probability"] = team_advantage_count / total_games

        return result

    def analyze_muestra_distribution(self) -> Dict[str, Any]:
        """
        Analyze the distribution of muestra cards across simulations.

        Returns:
            Dictionary with statistics about muestra distribution:
            - suit_distribution: Probability of each suit being the muestra
            - rank_distribution: Probability of each rank being the muestra
        """
        total_games = len(self.results.muestra_ranks)
        if total_games == 0:
            return {
                "suit_distribution": {},
                "rank_distribution": {},
            }

        # Analyze suit distribution
        suit_counts = {}
        for suit_value in self.results.muestra_suits:
            suit_counts[suit_value] = suit_counts.get(suit_value, 0) + 1

        suit_distribution = {
            suit.name: suit_counts.get(suit.value, 0) / total_games for suit in Suit
        }

        # Analyze rank distribution
        rank_counts = {}
        for rank_value in self.results.muestra_ranks:
            rank_counts[rank_value] = rank_counts.get(rank_value, 0) + 1

        rank_distribution = {
            rank.name: rank_counts.get(rank.value, 0) / total_games for rank in Rank
        }

        return {
            "suit_distribution": suit_distribution,
            "rank_distribution": rank_distribution,
        }

    def calculate_flower_stats(self) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics about flowers in the games.

        Returns:
            Dictionary with various statistics and probabilities
        """
        flower_counts = np.array(self.results.players_with_flower)

        # Basic stats
        basic_stats = {
            "mean": float(np.mean(flower_counts)),
            "median": float(np.median(flower_counts)),
            "std_dev": float(np.std(flower_counts)),
            "min": int(np.min(flower_counts)),
            "max": int(np.max(flower_counts)),
            "probability_at_least_one": float(
                np.sum(flower_counts > 0) / len(flower_counts)
            ),
            "probability_zero": float(np.sum(flower_counts == 0) / len(flower_counts)),
        }

        # Conditional probabilities
        conditional_probs = self.calculate_conditional_same_team_probability()

        # Team advantage
        team_advantage = self.calculate_team_advantage()

        # Multiple flowers probabilities
        multiple_flowers_prob = float(np.sum(flower_counts >= 2) / len(flower_counts))

        # Combine all stats
        result = {
            **basic_stats,
            "conditional_same_team_probability": conditional_probs[
                "when_multiple_flowers"
            ],
            "same_team_probability_by_flower_count": conditional_probs[
                "by_flower_count"
            ],
            "probability_multiple_flowers": multiple_flowers_prob,
            "team_advantage_probability": team_advantage["team_advantage_probability"],
            "flower_distribution_by_advantage": team_advantage[
                "flower_distribution_by_advantage"
            ],
        }

        return result

    def calculate_pieza_stats(self) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics about piezas in the games.

        Returns:
            Dictionary with various statistics and probabilities related to piezas
        """
        pieza_counts = np.array(self.results.players_with_pieza)

        # Skip if no games with piezas
        if len(pieza_counts) == 0:
            return {}

        # Basic stats
        basic_stats = {
            "mean": float(np.mean(pieza_counts)),
            "median": float(np.median(pieza_counts)),
            "std_dev": float(np.std(pieza_counts)),
            "min": int(np.min(pieza_counts)),
            "max": int(np.max(pieza_counts)),
            "probability_at_least_one": float(
                np.sum(pieza_counts > 0) / len(pieza_counts)
            ),
            "probability_zero": float(np.sum(pieza_counts == 0) / len(pieza_counts)),
        }

        # Conditional probabilities
        conditional_probs = self.calculate_conditional_same_team_pieza_probability()

        # Team advantage
        team_advantage = self.calculate_pieza_team_advantage()

        # Multiple piezas probabilities
        multiple_piezas_prob = float(np.sum(pieza_counts >= 2) / len(pieza_counts))

        # Combine all stats
        result = {
            **basic_stats,
            "conditional_same_team_probability": conditional_probs[
                "when_multiple_piezas"
            ],
            "same_team_probability_by_pieza_count": conditional_probs["by_pieza_count"],
            "probability_multiple_piezas": multiple_piezas_prob,
            "team_advantage_probability": team_advantage["team_advantage_probability"],
            "pieza_distribution_by_advantage": team_advantage[
                "pieza_distribution_by_advantage"
            ],
        }

        return result

    def calculate_combined_stats(self) -> Dict[str, Any]:
        """
        Calculate joint statistics about flowers and piezas.

        Returns:
            Dictionary with combined statistics
        """
        total_games = self.results.total_games
        if total_games == 0:
            return {}

        # Get individual stats first
        flower_stats = self.calculate_flower_stats()
        pieza_stats = self.calculate_pieza_stats()

        # Calculate joint probabilities
        joint_counts = {
            "both_flower_and_pieza": 0,
            "flower_only": 0,
            "pieza_only": 0,
            "neither": 0,
        }

        for i in range(total_games):
            has_flower = self.results.players_with_flower[i] > 0
            has_pieza = self.results.players_with_pieza[i] > 0

            if has_flower and has_pieza:
                joint_counts["both_flower_and_pieza"] += 1
            elif has_flower:
                joint_counts["flower_only"] += 1
            elif has_pieza:
                joint_counts["pieza_only"] += 1
            else:
                joint_counts["neither"] += 1

        # Convert to probabilities
        joint_probs = {key: count / total_games for key, count in joint_counts.items()}

        # Calculate conditional probabilities
        conditional_probs = {
            "pieza_given_flower": (
                joint_counts["both_flower_and_pieza"]
                / (joint_counts["both_flower_and_pieza"] + joint_counts["flower_only"])
                if (joint_counts["both_flower_and_pieza"] + joint_counts["flower_only"])
                > 0
                else 0
            ),
            "flower_given_pieza": (
                joint_counts["both_flower_and_pieza"]
                / (joint_counts["both_flower_and_pieza"] + joint_counts["pieza_only"])
                if (joint_counts["both_flower_and_pieza"] + joint_counts["pieza_only"])
                > 0
                else 0
            ),
        }

        return {
            "joint_probabilities": joint_probs,
            "conditional_probabilities": conditional_probs,
            "flower_stats": flower_stats,
            "pieza_stats": pieza_stats,
        }

    def calculate_confidence_interval(
        self, probability: float, sample_size: int, confidence: float = 0.95
    ) -> Dict[str, float]:
        """
        Calculate confidence interval for a probability estimate.

        Args:
            probability: Estimated probability
            sample_size: Number of samples used for estimation
            confidence: Confidence level (default 0.95 for 95% confidence)

        Returns:
            Dictionary with lower and upper bounds of the confidence interval
        """
        import scipy.stats as stats

        # Critical value for the given confidence level
        critical_value = stats.norm.ppf((1 + confidence) / 2)

        # Standard error
        std_error = (probability * (1 - probability) / sample_size) ** 0.5

        # Margin of error
        margin = critical_value * std_error

        return {
            "lower_bound": max(0, probability - margin),
            "upper_bound": min(1, probability + margin),
            "margin_of_error": margin,
        }
