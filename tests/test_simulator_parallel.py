"""Verify Simulator.run_simulations_parallel: games are independent, so
parallelizing across games should reproduce the sequential simulator's
aggregate statistics (not identical games, since each worker draws its own
seeded stream, but the same shape and comparable probabilities).
"""

from truco.simulation.simulator import Simulator

NUM_SIMULATIONS = 5_000


def test_parallel_matches_sequential_total_games() -> None:
    simulator = Simulator()
    result = simulator.run_simulations_parallel(NUM_SIMULATIONS, num_workers=4, seed=1)
    assert result.total_games == NUM_SIMULATIONS
    assert len(result.players_with_flower) == NUM_SIMULATIONS
    assert len(result.muestra_suits) == NUM_SIMULATIONS


def test_parallel_probability_of_flower_matches_sequential() -> None:
    sequential = Simulator().run_simulations(NUM_SIMULATIONS, seed=1)
    parallel = Simulator().run_simulations_parallel(
        NUM_SIMULATIONS, num_workers=4, seed=1
    )

    sequential_prob = sequential.games_with_flower / sequential.total_games
    parallel_prob = parallel.games_with_flower / parallel.total_games

    assert abs(sequential_prob - parallel_prob) < 0.05


def test_parallel_uneven_split_covers_all_simulations() -> None:
    # 5000 simulations over 3 workers doesn't divide evenly.
    simulator = Simulator()
    result = simulator.run_simulations_parallel(NUM_SIMULATIONS, num_workers=3, seed=7)
    assert result.total_games == NUM_SIMULATIONS
    assert len(result.players_with_pieza) == NUM_SIMULATIONS
