"""CLI for Truco Uruguayo Probability Simulator with more detailed statistics."""

import argparse
import json
import os
from typing import Any, Dict

from truco.analysis.statistics import StatisticsAnalyzer
from truco.simulation.simulator import Simulator
from truco.visualization.visualizer import Visualizer


def format_percentage(value: float) -> str:
    """Format a probability as a percentage with 2 decimal places."""
    return f"{value * 100:.2f}%"


class TrucoSimulatorCLI:
    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(
            description=" Truco Uruguayo Probability Simulator",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(
            "-n",
            "--num-simulations",
            type=int,
            default=10000,
            help="Number of game simulations to run",
        )

        parser.add_argument(
            "-p",
            "--players-per-team",
            type=int,
            default=3,
            help="Number of players per team",
        )

        parser.add_argument(
            "-t", "--num-teams", type=int, default=2, help="Number of teams"
        )

        parser.add_argument(
            "-s",
            "--seed",
            type=int,
            default=None,
            help="Random seed for reproducibility",
        )

        parser.add_argument(
            "-j", "--json", action="store_true", help="Output results in JSON format"
        )

        parser.add_argument(
            "-v",
            "--visualize",
            action="store_true",
            help="Generate visualizations of the simulation results",
        )

        parser.add_argument(
            "-o",
            "--output-dir",
            type=str,
            default="results",
            help="Directory to save visualization files",
        )

        parser.add_argument(
            "-d",
            "--detailed",
            action="store_true",
            help="Show detailed statistics with conditional probabilities",
        )

        return parser

    def run(self) -> None:
        """Run the CLI application."""
        args = self.parser.parse_args()

        # Run the simulation
        simulator = Simulator(args.players_per_team, args.num_teams)
        print(f"Running {args.num_simulations} simulations...")
        results = simulator.run_simulations(args.num_simulations, args.seed)

        # Analyze the results with statistics
        analyzer = StatisticsAnalyzer(results)
        stats = analyzer.calculate_flower_stats()
        flower_prob = analyzer.calculate_probability_of_flower()

        # Output the results
        if args.json:
            self._output_json(stats, flower_prob)
        else:
            self._output_text(stats, flower_prob, args.detailed)

        # Generate visualizations if requested
        if args.visualize:
            self._generate_visualizations(results, args.output_dir)

    def _output_json(
        self, stats: Dict[str, Any], flower_prob: Dict[int, float]
    ) -> None:
        """Output the results in JSON format."""
        output = {
            "flower_statistics": stats,
            "flower_probabilities": {str(k): v for k, v in flower_prob.items()},
        }
        print(json.dumps(output, indent=2))

    def _output_text(
        self,
        stats: Dict[str, Any],
        flower_prob: Dict[int, float],
        detailed: bool = False,
    ) -> None:
        """Output the results in human-readable text format."""
        print("\n=== Truco Uruguayo  Simulation Results ===\n")

        print("Basic Flower Statistics:")
        print(f"  Average players with flower: {stats['mean']:.2f}")
        print(f"  Standard deviation: {stats['std_dev']:.2f}")
        print(f"  Min/Max players with flower: {stats['min']}/{stats['max']}")
        print(
            f"  Probability of at least one flower: {format_percentage(stats['probability_at_least_one'])}"
        )
        print(
            f"  Probability of no flowers: {format_percentage(stats['probability_zero'])}"
        )
        print(
            f"  Probability of multiple flowers (2+): {format_percentage(stats['probability_multiple_flowers'])}"
        )

        if detailed:
            print("\nTeam Distribution Statistics:")
            print(
                f"  Probability of team advantage (one team has more flowers): {format_percentage(stats['team_advantage_probability'])}"
            )

            print("\nConditional Probabilities:")
            print(
                f"  When multiple players have flowers, probability they're all in same team: {format_percentage(stats['conditional_same_team_probability'])}"
            )

            print("\nSame Team Probability by Flower Count:")
            for count, prob in sorted(
                stats["same_team_probability_by_flower_count"].items()
            ):
                print(
                    f"  When exactly {count} players have flowers, probability all in same team: {format_percentage(prob)}"
                )

            print("\nFlower Advantage Distribution:")
            for adv, prob in sorted(stats["flower_distribution_by_advantage"].items()):
                team = "Team 0" if adv > 0 else "Team 1"
                if adv == 0:
                    print(f"  Equal flowers between teams: {format_percentage(prob)}")
                else:
                    print(
                        f"  {team} has {abs(adv)} more flower(s): {format_percentage(prob)}"
                    )

        print("\nProbability Distribution (number of players with flower):")
        for num_players, prob in sorted(flower_prob.items()):
            print(f"  {num_players} players: {format_percentage(prob)}")

    def _generate_visualizations(self, results, output_dir: str) -> None:
        """Generate and save visualizations of the simulation results."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Initialize visualizer
            visualizer = Visualizer(results)

            # Generate visualizations
            print("\nGenerating visualizations...")

            # Flower distribution plot
            flower_dist_path = os.path.join(output_dir, "flower_distribution.png")
            visualizer.plot_flower_distribution(save_path=flower_dist_path)
            print(f"  Saved flower distribution plot to {flower_dist_path}")

            # Team flower distribution plot
            team_dist_path = os.path.join(output_dir, "team_flower_distribution.png")
            visualizer.plot_team_advantage(save_path=team_dist_path)
            print(f"  Saved team flower distribution plot to {team_dist_path}")

            # Same team probability plot
            same_team_path = os.path.join(output_dir, "same_team_probability.png")
            visualizer.plot_conditional_same_team_probability(save_path=same_team_path)
            print(f"  Saved same team probability plot to {same_team_path}")

            # Pieza plots
            pieza_dist_path = os.path.join(output_dir, "pieza_distribution.png")
            visualizer.plot_pieza_distribution(save_path=pieza_dist_path)
            print(f"  Saved pieza distribution plot to {pieza_dist_path}")

            pieza_team_path = os.path.join(output_dir, "pieza_team_advantage.png")
            visualizer.plot_pieza_team_advantage(save_path=pieza_team_path)
            print(f"  Saved pieza team advantage plot to {pieza_team_path}")

            # Joint probability plot
            joint_prob_path = os.path.join(output_dir, "joint_probabilities.png")
            visualizer.plot_joint_flower_pieza_probability(save_path=joint_prob_path)
            print(f"  Saved joint probabilities plot to {joint_prob_path}")

            # Muestra distribution plot
            muestra_path = os.path.join(output_dir, "muestra_distribution.png")
            visualizer.plot_muestra_distribution(save_path=muestra_path)
            print(f"  Saved muestra distribution plot to {muestra_path}")

            print("Visualizations complete.")

        except Exception as e:
            print(f"Error generating visualizations: {e}")
            print("Make sure matplotlib is installed: pip install matplotlib")


def main():
    """Entry point for the Truco simulator CLI."""
    cli = TrucoSimulatorCLI()
    cli.run()


if __name__ == "__main__":
    main()
