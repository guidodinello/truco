"""Sanity check: the muestra card should be uniformly distributed.

The muestra is drawn from a well-shuffled 40-card deck, so over many games
its suit should be ~uniform over 4 values and its rank ~uniform over 10
values. A chi-square goodness-of-fit test catches a broken/biased shuffle
without requiring exact counts.
"""

from collections import Counter

import pytest

from truco.simulation.simulator import Simulator

NUM_SIMULATIONS = 20_000
NUM_SUITS = 4
NUM_RANKS = 10
# Generous threshold: with correct df, p < 0.001 under H0 is already rare
# (chi-square critical value for df=3 at alpha=0.001 is ~16.3, df=9 is ~27.9).
CHI_SQUARE_CRITICAL = {NUM_SUITS - 1: 16.3, NUM_RANKS - 1: 27.9}


def _chi_square_statistic(observed_counts: list[int], expected: float) -> float:
    return sum((count - expected) ** 2 / expected for count in observed_counts)


@pytest.mark.parametrize("seed", [None, 42])
def test_muestra_suit_distribution_is_uniform(seed: int | None) -> None:
    simulator = Simulator()
    results = simulator.run_simulations(NUM_SIMULATIONS, seed=seed)

    counts = Counter(results.muestra_suits)
    assert len(counts) == NUM_SUITS

    expected = NUM_SIMULATIONS / NUM_SUITS
    chi_square = _chi_square_statistic(list(counts.values()), expected)
    assert chi_square < CHI_SQUARE_CRITICAL[NUM_SUITS - 1]


@pytest.mark.parametrize("seed", [None, 42])
def test_muestra_rank_distribution_is_uniform(seed: int | None) -> None:
    simulator = Simulator()
    results = simulator.run_simulations(NUM_SIMULATIONS, seed=seed)

    counts = Counter(results.muestra_ranks)
    assert len(counts) == NUM_RANKS

    expected = NUM_SIMULATIONS / NUM_RANKS
    chi_square = _chi_square_statistic(list(counts.values()), expected)
    assert chi_square < CHI_SQUARE_CRITICAL[NUM_RANKS - 1]
