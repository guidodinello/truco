#!/usr/bin/env python3
"""
Example script demonstrating how to use the Truco Uruguayo simulator.
This runs simulations and analyzes probabilities of flowers and piezas.
"""

import argparse
import os

from truco.analysis.statistics import StatisticsAnalyzer
from truco.simulation.simulator import SimulationResult, Simulator
from truco.visualization.visualizer import Visualizer


def main():
    """Run simulations and generate statistics and visualizations."""
    parser = argparse.ArgumentParser(
        description="Truco Uruguayo Probability Simulator",
    )
    parser.add_argument(
        "-n",
        "--num-simulations",
        type=int,
        default=100_000,
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
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Generate visualizations",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="results",
        help="Directory to save visualization files",
    )

    args = parser.parse_args()

    # Create output directory if visualizing
    if args.visualize:
        os.makedirs(args.output_dir, exist_ok=True)

    print(f"Running {args.num_simulations} simulations...")
    print(
        f"Configuration: {args.players_per_team} players per team, {args.num_teams} teams"
    )

    from tqdm import tqdm

    print(f"Running {args.num_simulations} simulations...")
    print(
        f"Configuration: {args.players_per_team} players per team, {args.num_teams} teams"
    )

    # Run simulations with progress bar
    simulator = Simulator(args.players_per_team, args.num_teams)

    # Use parallel implementation if available and num_simulations is large
    if args.num_simulations > 10000 and hasattr(simulator, "run_simulations_parallel"):
        results = simulator.run_simulations_parallel(
            args.num_simulations, seed=args.seed
        )
    else:
        # Fallback to sequential with progress bar
        results = SimulationResult(
            total_games=args.num_simulations,
            players_with_flower=[],
            flower_distribution=[],
            all_flowers_same_team=[],
            players_with_pieza=[],
            pieza_distribution=[],
            all_piezas_same_team=[],
            muestra_ranks=[],
            muestra_suits=[],
        )

        game = simulator.game

        for i in tqdm(range(args.num_simulations), desc="Simulating games"):
            game_seed = None if args.seed is None else args.seed + i
            game.deal_cards(seed=game_seed)

            results.players_with_flower.append(game.count_players_with_flower())
            results.flower_distribution.append(game.get_flower_distribution())
            results.all_flowers_same_team.append(game.is_all_flowers_in_same_team())

            piezas_by_team = game.get_pieza_distribution()
            players_with_pieza_count = game.count_players_with_piezas()
            results.players_with_pieza.append(players_with_pieza_count)
            results.pieza_distribution.append(piezas_by_team)
            all_piezas_same = (
                any(
                    count == players_with_pieza_count
                    for count in piezas_by_team.values()
                )
                if players_with_pieza_count > 0
                else False
            )
            results.all_piezas_same_team.append(all_piezas_same)

            results.muestra_ranks.append(game.muestra.rank.value)
            results.muestra_suits.append(game.muestra.suit.value)

    # Analyze results
    analyzer = StatisticsAnalyzer(results)

    # Display flower statistics
    flower_stats = analyzer.calculate_flower_stats()
    print("\n=== Flower Statistics ===")
    print(f"Average players with flower: {flower_stats['mean']:.2f}")
    print(
        f"Probability of at least one flower: {flower_stats['probability_at_least_one']:.1%}"
    )
    print(
        f"Probability of multiple flowers: {flower_stats['probability_multiple_flowers']:.1%}"
    )
    print(
        f"When multiple flowers occur, probability all in same team: {flower_stats['conditional_same_team_probability']:.1%}"
    )

    # Display pieza statistics
    pieza_stats = analyzer.calculate_pieza_stats()
    if pieza_stats:  # Check if we have pieza data
        print("\n=== Pieza Statistics ===")
        print(f"Average players with pieza: {pieza_stats['mean']:.2f}")
        print(
            f"Probability of at least one pieza: {pieza_stats['probability_at_least_one']:.1%}"
        )
        print(
            f"Probability of multiple piezas: {pieza_stats['probability_multiple_piezas']:.1%}"
        )
        print(
            f"When multiple piezas occur, probability all in same team: {pieza_stats['conditional_same_team_probability']:.1%}"
        )

    # Display combined statistics
    combined_stats = analyzer.calculate_combined_stats()
    if combined_stats:
        joint_probs = combined_stats["joint_probabilities"]
        cond_probs = combined_stats["conditional_probabilities"]

        print("\n=== Combined Statistics ===")
        print(
            f"Probability of both flower and pieza: {joint_probs['both_flower_and_pieza']:.1%}"
        )
        print(
            f"Probability of flower given pieza: {cond_probs['flower_given_pieza']:.1%}"
        )
        print(
            f"Probability of pieza given flower: {cond_probs['pieza_given_flower']:.1%}"
        )

    # Generate visualizations if requested
    if args.visualize:
        print("\nGenerating visualizations...")
        visualizer = Visualizer(results)
        visualizer.generate_all_plots(args.output_dir)
        print(f"Visualizations saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
