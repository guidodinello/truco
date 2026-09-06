"""Visualization tools for Truco Uruguayo simulation results."""

import os
from typing import Optional

import matplotlib.pyplot as plt

from truco.domain.card import Suit
from truco.simulation.simulator import SimulationResult


class Visualizer:
    """Class for creating visualizations of Truco simulation results."""

    def __init__(self, results: SimulationResult):
        """Initialize with simulation results."""
        self.results = results

        # Configure plot style
        plt.style.use("seaborn-v0_8-darkgrid")

    def plot_flower_distribution(self, save_path: Optional[str] = None) -> None:
        """
        Plot the distribution of players with flowers across all simulated games.

        Args:
            save_path: Optional path to save the plot to a file
        """
        flower_counts = self.results.players_with_flower

        # Skip if no games
        if not flower_counts:
            print("No games found for flower distribution.")
            return

        # Calculate distribution
        max_flowers = max(flower_counts)
        distribution = {}
        for i in range(max_flowers + 1):
            distribution[i] = flower_counts.count(i) / len(flower_counts)

        # Create plot
        plt.figure(figsize=(10, 6))

        plt.bar(distribution.keys(), distribution.values(), color="#5DA5DA", alpha=0.8)

        # Add percentage labels on bars
        for count, prob in distribution.items():
            plt.text(count, prob + 0.01, f"{prob:.1%}", ha="center", fontweight="bold")

        plt.xlabel("Number of Players with Flowers")
        plt.ylabel("Probability")
        plt.title("Distribution of Players with Flowers")

        plt.xticks(list(range(max_flowers + 1)))
        plt.ylim(0, max(distribution.values()) * 1.2)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_pieza_distribution(self, save_path: Optional[str] = None) -> None:
        """
        Plot the distribution of players with piezas across all simulated games.

        Args:
            save_path: Optional path to save the plot to a file
        """
        pieza_counts = self.results.players_with_pieza

        # Skip if no games
        if not pieza_counts:
            print("No games found for pieza distribution.")
            return

        # Calculate distribution
        max_piezas = max(pieza_counts)
        distribution = {}
        for i in range(max_piezas + 1):
            distribution[i] = pieza_counts.count(i) / len(pieza_counts)

        # Create plot
        plt.figure(figsize=(10, 6))

        plt.bar(distribution.keys(), distribution.values(), color="#60BD68", alpha=0.8)

        # Add percentage labels on bars
        for count, prob in distribution.items():
            plt.text(count, prob + 0.01, f"{prob:.1%}", ha="center", fontweight="bold")

        plt.xlabel("Number of Players with Piezas")
        plt.ylabel("Probability")
        plt.title("Distribution of Players with Piezas")

        plt.xticks(list(range(max_piezas + 1)))
        plt.ylim(0, max(distribution.values()) * 1.2)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_conditional_same_team_probability(
        self, save_path: Optional[str] = None
    ) -> None:
        """
        Plot the probability of all flowers being in the same team,
        conditioned on the number of players with flowers.

        Args:
            save_path: Optional path to save the plot to a file
        """
        flower_counts = self.results.players_with_flower
        same_team_flags = self.results.all_flowers_same_team

        # Calculate probabilities for each flower count
        max_flowers = max(flower_counts) if flower_counts else 0

        # Skip if no flowers found
        if max_flowers == 0:
            print("No flowers found in any simulations.")
            return

        # Calculate conditional probabilities
        same_team_probs = []
        counts = []

        for count in range(2, max_flowers + 1):
            # Find games with exactly this many flowers
            count_indices = [i for i, fc in enumerate(flower_counts) if fc == count]

            if not count_indices:
                continue

            # Count how many had all flowers in same team
            same_team_count = sum(1 for i in count_indices if same_team_flags[i])

            # Calculate probability
            prob = same_team_count / len(count_indices) if count_indices else 0

            same_team_probs.append(prob)
            counts.append(count)

        # Skip if no relevant data
        if not counts:
            print("No games with multiple flowers found.")
            return

        # Create the plot
        plt.figure(figsize=(10, 6))

        # Bar plot
        plt.bar(counts, same_team_probs, color="#5DA5DA", alpha=0.8)

        # Add labels
        for i, count in enumerate(counts):
            plt.text(
                count,
                same_team_probs[i] + 0.03,
                f"{same_team_probs[i]:.1%}",
                ha="center",
                fontweight="bold",
            )

        plt.xlabel("Number of Players with Flowers")
        plt.ylabel("Probability All Flowers in Same Team")
        plt.title(
            "Conditional Probability: All Flowers in Same Team\nGiven N Players Have Flowers"
        )

        plt.xticks(counts)
        plt.ylim(0, 1.1)  # Set y-axis to range from 0 to 110%

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_conditional_same_team_pieza_probability(
        self, save_path: Optional[str] = None
    ) -> None:
        """
        Plot the probability of all piezas being in the same team,
        conditioned on the number of players with piezas.

        Args:
            save_path: Optional path to save the plot to a file
        """
        pieza_counts = self.results.players_with_pieza
        same_team_flags = self.results.all_piezas_same_team

        # Calculate probabilities for each pieza count
        max_piezas = max(pieza_counts) if pieza_counts else 0

        # Skip if no piezas found
        if max_piezas == 0:
            print("No piezas found in any simulations.")
            return

        # Calculate conditional probabilities
        same_team_probs = []
        counts = []

        for count in range(2, max_piezas + 1):
            # Find games with exactly this many piezas
            count_indices = [i for i, pc in enumerate(pieza_counts) if pc == count]

            if not count_indices:
                continue

            # Count how many had all piezas in same team
            same_team_count = sum(1 for i in count_indices if same_team_flags[i])

            # Calculate probability
            prob = same_team_count / len(count_indices) if count_indices else 0

            same_team_probs.append(prob)
            counts.append(count)

        # Skip if no relevant data
        if not counts:
            print("No games with multiple piezas found.")
            return

        # Create the plot
        plt.figure(figsize=(10, 6))

        # Bar plot
        plt.bar(counts, same_team_probs, color="#60BD68", alpha=0.8)

        # Add labels
        for i, count in enumerate(counts):
            plt.text(
                count,
                same_team_probs[i] + 0.03,
                f"{same_team_probs[i]:.1%}",
                ha="center",
                fontweight="bold",
            )

        plt.xlabel("Number of Players with Piezas")
        plt.ylabel("Probability All Piezas in Same Team")
        plt.title(
            "Conditional Probability: All Piezas in Same Team\nGiven N Players Have Piezas"
        )

        plt.xticks(counts)
        plt.ylim(0, 1.1)  # Set y-axis to range from 0 to 110%

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_team_advantage(self, save_path: Optional[str] = None) -> None:
        """
        Plot the distribution of flower advantages between teams.

        Args:
            save_path: Optional path to save the plot to a file
        """
        # Skip if no flower distribution data
        if not self.results.flower_distribution:
            print("No flower distribution data found.")
            return

        # Get number of teams from first game
        num_teams = len(self.results.flower_distribution[0])

        # Skip if not a two-team game
        if num_teams != 2:
            print("Team advantage plot only supports two-team games.")
            return

        # Calculate flower count differences for each game
        advantages = []

        for game_distrib in self.results.flower_distribution:
            team0_flowers = game_distrib.get(0, 0)
            team1_flowers = game_distrib.get(1, 0)
            advantage = team0_flowers - team1_flowers
            advantages.append(advantage)

        # Calculate advantage distribution
        advantage_values = sorted(set(advantages))
        advantage_counts = [advantages.count(adv) for adv in advantage_values]
        advantage_probs = [count / len(advantages) for count in advantage_counts]

        # Create plot
        plt.figure(figsize=(12, 6))

        # Bar colors
        colors = [
            "#FAA43A" if adv < 0 else "#5DA5DA" if adv > 0 else "#B2912F"
            for adv in advantage_values
        ]

        # Create bar plot
        plt.bar(advantage_values, advantage_probs, color=colors, alpha=0.8)

        # Add percentage labels
        for i, adv in enumerate(advantage_values):
            if (
                advantage_probs[i] > 0.01
            ):  # Only label bars with significant probability
                plt.text(
                    adv,
                    advantage_probs[i] + 0.01,
                    f"{advantage_probs[i]:.1%}",
                    ha="center",
                    fontsize=9,
                )

        plt.xlabel("Flower Advantage (Team 0 - Team 1)")
        plt.ylabel("Probability")
        plt.title("Distribution of Flower Advantage Between Teams")

        # Add legend
        from matplotlib.patches import Patch

        legend_elements = [
            Patch(facecolor="#5DA5DA", label="Team 0 Advantage"),
            Patch(facecolor="#B2912F", label="Equal"),
            Patch(facecolor="#FAA43A", label="Team 1 Advantage"),
        ]
        plt.legend(handles=legend_elements, loc="upper right")

        # Set x-axis ticks
        plt.xticks(advantage_values)

        # Add grid
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_pieza_team_advantage(self, save_path: Optional[str] = None) -> None:
        """
        Plot the distribution of pieza advantages between teams.

        Args:
            save_path: Optional path to save the plot to a file
        """
        # Skip if no pieza distribution data
        if not self.results.pieza_distribution:
            print("No pieza distribution data found.")
            return

        # Get number of teams from first game
        num_teams = len(self.results.pieza_distribution[0])

        # Skip if not a two-team game
        if num_teams != 2:
            print("Team advantage plot only supports two-team games.")
            return

        # Calculate pieza count differences for each game
        advantages = []

        for game_distrib in self.results.pieza_distribution:
            team0_piezas = game_distrib.get(0, 0)
            team1_piezas = game_distrib.get(1, 0)
            advantage = team0_piezas - team1_piezas
            advantages.append(advantage)

        # Calculate advantage distribution
        advantage_values = sorted(set(advantages))
        advantage_counts = [advantages.count(adv) for adv in advantage_values]
        advantage_probs = [count / len(advantages) for count in advantage_counts]

        # Create plot
        plt.figure(figsize=(12, 6))

        # Bar colors
        colors = [
            "#FAA43A" if adv < 0 else "#60BD68" if adv > 0 else "#B2912F"
            for adv in advantage_values
        ]

        # Create bar plot
        plt.bar(advantage_values, advantage_probs, color=colors, alpha=0.8)

        # Add percentage labels
        for i, adv in enumerate(advantage_values):
            if (
                advantage_probs[i] > 0.01
            ):  # Only label bars with significant probability
                plt.text(
                    adv,
                    advantage_probs[i] + 0.01,
                    f"{advantage_probs[i]:.1%}",
                    ha="center",
                    fontsize=9,
                )

        plt.xlabel("Pieza Advantage (Team 0 - Team 1)")
        plt.ylabel("Probability")
        plt.title("Distribution of Pieza Advantage Between Teams")

        # Add legend
        from matplotlib.patches import Patch

        legend_elements = [
            Patch(facecolor="#60BD68", label="Team 0 Advantage"),
            Patch(facecolor="#B2912F", label="Equal"),
            Patch(facecolor="#FAA43A", label="Team 1 Advantage"),
        ]
        plt.legend(handles=legend_elements, loc="upper right")

        # Set x-axis ticks
        plt.xticks(advantage_values)

        # Add grid
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_multiple_flowers_probability(
        self, save_path: Optional[str] = None
    ) -> None:
        """
        Plot the probability of different numbers of players having flowers,
        focusing on games with 2+ players with flowers.

        Args:
            save_path: Optional path to save the plot to a file
        """
        flower_counts = self.results.players_with_flower
        max_flowers = max(flower_counts) if flower_counts else 0

        # Skip if no flowers found
        if max_flowers < 2:
            print("No games with multiple flowers found.")
            return

        # Calculate probabilities for 2+ flowers
        multi_flowers = {}
        total_games = len(flower_counts)

        for count in range(2, max_flowers + 1):
            games_with_count = flower_counts.count(count)
            multi_flowers[count] = games_with_count / total_games

        # Create plot
        plt.figure(figsize=(9, 6))

        counts = list(multi_flowers.keys())
        probs = list(multi_flowers.values())

        plt.bar(counts, probs, color="#5DA5DA", alpha=0.8)

        for i, count in enumerate(counts):
            if probs[i] > 0.0005:  # Only label bars with visible probability
                plt.text(
                    count, probs[i] + 0.001, f"{probs[i]:.2%}", ha="center", fontsize=10
                )

        plt.xlabel("Number of Players with Flowers")
        plt.ylabel("Probability")
        plt.title("Probability of Multiple Players Having Flowers")

        # Set x-axis ticks
        plt.xticks(counts)

        # Add grid
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_multiple_piezas_probability(self, save_path: Optional[str] = None) -> None:
        """
        Plot the probability of different numbers of players having piezas,
        focusing on games with 2+ players with piezas.

        Args:
            save_path: Optional path to save the plot to a file
        """
        pieza_counts = self.results.players_with_pieza
        max_piezas = max(pieza_counts) if pieza_counts else 0

        # Skip if no piezas found
        if max_piezas < 2:
            print("No games with multiple piezas found.")
            return

        # Calculate probabilities for 2+ piezas
        multi_piezas = {}
        total_games = len(pieza_counts)

        for count in range(2, max_piezas + 1):
            games_with_count = pieza_counts.count(count)
            multi_piezas[count] = games_with_count / total_games

        # Create plot
        plt.figure(figsize=(9, 6))

        counts = list(multi_piezas.keys())
        probs = list(multi_piezas.values())

        plt.bar(counts, probs, color="#60BD68", alpha=0.8)

        for i, count in enumerate(counts):
            if probs[i] > 0.0005:  # Only label bars with visible probability
                plt.text(
                    count, probs[i] + 0.001, f"{probs[i]:.2%}", ha="center", fontsize=10
                )

        plt.xlabel("Number of Players with Piezas")
        plt.ylabel("Probability")
        plt.title("Probability of Multiple Players Having Piezas")

        # Set x-axis ticks
        plt.xticks(counts)

        # Add grid
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_muestra_distribution(self, save_path: Optional[str] = None) -> None:
        """
        Plot the distribution of muestra cards across simulations.

        Args:
            save_path: Optional path to save the plot to a file
        """
        if not self.results.muestra_ranks or not self.results.muestra_suits:
            print("No muestra data available.")
            return

        # Count suit distribution
        suit_counts = {}
        for suit_val in self.results.muestra_suits:
            suit_counts[suit_val] = suit_counts.get(suit_val, 0) + 1

        # Convert to names and probabilities
        suit_names = {s.value: s.name for s in Suit}
        suit_probs = {
            suit_names.get(suit_val, f"Unknown ({suit_val})"): count
            / len(self.results.muestra_suits)
            for suit_val, count in suit_counts.items()
        }

        # Create plot
        plt.figure(figsize=(10, 6))

        # Sort by probability to make plot more readable
        sorted_suits = sorted(suit_probs.items(), key=lambda x: x[1], reverse=True)
        names = [item[0] for item in sorted_suits]
        probs = [item[1] for item in sorted_suits]

        plt.bar(names, probs, color="#F15854", alpha=0.8)

        # Add percentage labels
        for i, name in enumerate(names):
            plt.text(
                i, probs[i] + 0.01, f"{probs[i]:.1%}", ha="center", fontweight="bold"
            )

        plt.xlabel("Muestra Suit")
        plt.ylabel("Probability")
        plt.title("Distribution of Muestra Suits")

        plt.xticks(rotation=45)
        plt.ylim(0, max(probs) * 1.2)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def plot_joint_flower_pieza_probability(
        self, save_path: Optional[str] = None
    ) -> None:
        """
        Plot the joint probabilities of having flowers and piezas in the game.

        Args:
            save_path: Optional path to save the plot to a file
        """
        if not self.results.players_with_flower or not self.results.players_with_pieza:
            print("No data available for joint probabilities.")
            return

        # Calculate joint counts
        joint_counts = {
            "Both Flower and Pieza": 0,
            "Flower Only": 0,
            "Pieza Only": 0,
            "Neither": 0,
        }

        total_games = self.results.total_games

        for i in range(total_games):
            has_flower = self.results.players_with_flower[i] > 0
            has_pieza = self.results.players_with_pieza[i] > 0

            if has_flower and has_pieza:
                joint_counts["Both Flower and Pieza"] += 1
            elif has_flower:
                joint_counts["Flower Only"] += 1
            elif has_pieza:
                joint_counts["Pieza Only"] += 1
            else:
                joint_counts["Neither"] += 1

        # Convert to probabilities
        joint_probs = {k: v / total_games for k, v in joint_counts.items()}

        # Create plot
        plt.figure(figsize=(10, 6))

        # Define colors and labels
        categories = list(joint_probs.keys())
        values = list(joint_probs.values())
        colors = ["#4D4D4D", "#5DA5DA", "#60BD68", "#F15854"]

        plt.bar(categories, values, color=colors, alpha=0.8)

        # Add percentage labels
        for i, cat in enumerate(categories):
            plt.text(
                i, values[i] + 0.01, f"{values[i]:.1%}", ha="center", fontweight="bold"
            )

        plt.xlabel("Game Outcome")
        plt.ylabel("Probability")
        plt.title("Joint Probability of Flowers and Piezas")

        plt.xticks(rotation=15)
        plt.ylim(0, max(values) * 1.2)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.tight_layout()
        # Only try to show plot in interactive environment
        if plt.isinteractive():
            plt.show()

    def generate_all_plots(self, output_dir: str) -> None:
        """
        Generate all available visualizations and save them to the specified directory.

        Args:
            output_dir: Directory to save the plot files
        """
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate all plots
        plots = [
            ("flower_distribution.png", self.plot_flower_distribution),
            ("pieza_distribution.png", self.plot_pieza_distribution),
            (
                "conditional_same_team_probability.png",
                self.plot_conditional_same_team_probability,
            ),
            (
                "conditional_same_team_pieza_probability.png",
                self.plot_conditional_same_team_pieza_probability,
            ),
            ("team_advantage.png", self.plot_team_advantage),
            ("pieza_team_advantage.png", self.plot_pieza_team_advantage),
            (
                "multiple_flowers_probability.png",
                self.plot_multiple_flowers_probability,
            ),
            ("multiple_piezas_probability.png", self.plot_multiple_piezas_probability),
            ("muestra_distribution.png", self.plot_muestra_distribution),
            (
                "joint_flower_pieza_probability.png",
                self.plot_joint_flower_pieza_probability,
            ),
        ]

        # Generate each plot and save it
        for filename, plot_method in plots:
            try:
                save_path = os.path.join(output_dir, filename)
                plot_method(save_path=save_path)
                print(f"Saved {filename}")
            except Exception as e:
                print(f"Error generating {filename}: {e}")
