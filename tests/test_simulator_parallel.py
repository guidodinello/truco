"""Verify Simulator.run_simulations_parallel: games are independent, so
parallelizing across games should reproduce the sequential simulator's
results exactly for a given seed. Each worker gets a contiguous, disjoint
slice of the global seed sequence (see
truco.simulation.simulator._partition_simulations), so the union of
per-worker seeds equals the sequential simulator's own seed..seed+n-1 range
and the two runs deal bit-identical hands.
"""

from truco.simulation.simulator import Simulator, _partition_simulations

NUM_SIMULATIONS = 5_000


def test_parallel_matches_sequential_total_games() -> None:
    simulator = Simulator()
    result = simulator.run_simulations_parallel(NUM_SIMULATIONS, num_workers=4, seed=1)
    assert result.total_games == NUM_SIMULATIONS
    assert len(result.players_with_flower) == NUM_SIMULATIONS
    assert len(result.muestra_suits) == NUM_SIMULATIONS


def test_parallel_uneven_split_covers_all_simulations() -> None:
    # 5000 simulations over 3 workers doesn't divide evenly.
    simulator = Simulator()
    result = simulator.run_simulations_parallel(NUM_SIMULATIONS, num_workers=3, seed=7)
    assert result.total_games == NUM_SIMULATIONS
    assert len(result.players_with_pieza) == NUM_SIMULATIONS


def test_worker_seeds_partition_the_sequential_seed_range() -> None:
    """The union of per-worker seeds must equal the sequential simulator's
    own seed..seed+n-1 range, with no overlap. Under the old fixed-stride
    scheme (seed + i * 1000), this fails as soon as a worker runs more than
    1000 games -- e.g. n=5000, workers=4 (1250 games/worker) yielded only
    4250 distinct seeds instead of 5000."""
    seed = 1
    for num_simulations, num_workers in (
        (NUM_SIMULATIONS, 3),
        (NUM_SIMULATIONS, 4),
        (NUM_SIMULATIONS, 8),
    ):
        sims_per_worker, worker_seeds = _partition_simulations(
            num_simulations, num_workers, seed
        )

        flattened_seeds: list[int] = []
        for sims, worker_seed in zip(sims_per_worker, worker_seeds, strict=True):
            assert worker_seed is not None
            flattened_seeds.extend(worker_seed + j for j in range(sims))

        assert len(flattened_seeds) == num_simulations
        assert len(set(flattened_seeds)) == num_simulations
        assert set(flattened_seeds) == set(range(seed, seed + num_simulations))


def test_partition_simulations_with_no_seed_leaves_workers_unseeded() -> None:
    sims_per_worker, worker_seeds = _partition_simulations(
        NUM_SIMULATIONS, num_workers=4, seed=None
    )
    assert sum(sims_per_worker) == NUM_SIMULATIONS
    assert worker_seeds == [None] * 4


def test_parallel_reproduces_sequential_exactly() -> None:
    """At num_workers=4, each worker deals 1250 games -- more than the old
    1000-game stride -- so this fails loudly under the previous
    implementation, which would re-deal duplicate hands across workers."""
    sequential = Simulator().run_simulations(NUM_SIMULATIONS, seed=1)
    parallel = Simulator().run_simulations_parallel(
        NUM_SIMULATIONS, num_workers=4, seed=1
    )

    assert parallel.total_games == sequential.total_games
    assert parallel.players_with_flower == sequential.players_with_flower
    assert parallel.flower_distribution == sequential.flower_distribution
    assert parallel.all_flowers_same_team == sequential.all_flowers_same_team
    assert parallel.players_with_pieza == sequential.players_with_pieza
    assert parallel.pieza_distribution == sequential.pieza_distribution
    assert parallel.all_piezas_same_team == sequential.all_piezas_same_team
    assert parallel.muestra_ranks == sequential.muestra_ranks
    assert parallel.muestra_suits == sequential.muestra_suits


def test_unseeded_parallel_still_runs() -> None:
    simulator = Simulator()
    result = simulator.run_simulations_parallel(NUM_SIMULATIONS, num_workers=4)
    assert result.total_games == NUM_SIMULATIONS
