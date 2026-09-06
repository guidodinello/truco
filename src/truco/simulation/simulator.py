import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypedDict

from truco.domain.game import Game


class _RawSimulationData(TypedDict):
    """Shape of one worker's raw simulation output, before it's combined
    into a SimulationResult. Kept as a TypedDict (not SimulationResult
    itself) since a worker never knows total_games across all workers."""

    players_with_flower: List[int]
    flower_distribution: List[Dict[int, int]]
    all_flowers_same_team: List[bool]
    players_with_pieza: List[int]
    pieza_distribution: List[Dict[int, int]]
    all_piezas_same_team: List[bool]
    muestra_ranks: List[int]
    muestra_suits: List[int]


@dataclass(frozen=True, slots=True)
class SimulationResult:
    total_games: int
    players_with_flower: List[int]  # Count per game
    flower_distribution: List[Dict[int, int]]  # Team distribution per game
    all_flowers_same_team: List[bool]  # Flag per game
    players_with_pieza: List[int]  # Count per game
    pieza_distribution: List[Dict[int, int]]  # Team distribution per game
    all_piezas_same_team: List[bool]  # Flag per game
    muestra_ranks: List[int]  # Rank of muestra per game
    muestra_suits: List[int]  # Suit of muestra per game

    @property
    def games_with_flower(self) -> int:
        """Count games where at least one player had a flower."""
        return sum(1 for count in self.players_with_flower if count > 0)

    @property
    def games_with_all_flowers_same_team(self) -> int:
        """Count games where all flowers were in the same team."""
        return sum(self.all_flowers_same_team)

    @property
    def games_with_pieza(self) -> int:
        """Count games where at least one player had a pieza."""
        return sum(1 for count in self.players_with_pieza if count > 0)

    @property
    def games_with_all_piezas_same_team(self) -> int:
        """Count games where all piezas were in the same team."""
        return sum(self.all_piezas_same_team)


# Define the worker function at module level (not inside another function)
# to make it picklable for multiprocessing
def worker_function(
    num_sims: int,
    worker_seed: Optional[int],
    players_per_team: int,
    num_teams: int,
) -> _RawSimulationData:
    game = Game(players_per_team, num_teams)

    players_with_flower = []
    flower_distribution = []
    all_flowers_same_team = []
    players_with_pieza = []
    pieza_distribution = []
    all_piezas_same_team = []
    muestra_ranks = []
    muestra_suits = []

    for i in range(num_sims):
        game_seed = None if worker_seed is None else worker_seed + i
        game.deal_cards(seed=game_seed)

        players_with_flower.append(game.count_players_with_flower())
        flower_distribution.append(game.get_flower_distribution())
        all_flowers_same_team.append(game.is_all_flowers_in_same_team())

        players_with_pieza.append(game.count_players_with_piezas())
        pieza_distribution.append(game.get_pieza_distribution())

        piezas_by_team = game.get_pieza_distribution()
        players_with_pieza_count = game.count_players_with_piezas()
        all_piezas_same = (
            any(count == players_with_pieza_count for count in piezas_by_team.values())
            if players_with_pieza_count > 0
            else False
        )
        all_piezas_same_team.append(all_piezas_same)

        muestra = game.muestra
        if muestra is None:
            raise RuntimeError("deal_cards() must be called before reading its muestra")
        muestra_ranks.append(muestra.rank.value)
        muestra_suits.append(muestra.suit.value)

    return {
        "players_with_flower": players_with_flower,
        "flower_distribution": flower_distribution,
        "all_flowers_same_team": all_flowers_same_team,
        "players_with_pieza": players_with_pieza,
        "pieza_distribution": pieza_distribution,
        "all_piezas_same_team": all_piezas_same_team,
        "muestra_ranks": muestra_ranks,
        "muestra_suits": muestra_suits,
    }


class Simulator:
    def __init__(self, num_players_per_team: int = 3, num_teams: int = 2):
        self.game = Game(num_players_per_team, num_teams)

    def run_simulations(
        self, num_simulations: int, seed: Optional[int] = None
    ) -> SimulationResult:
        """Run a specified number of game simulations."""
        if seed is not None:
            random.seed(seed)

        players_with_flower = []
        flower_distribution = []
        all_flowers_same_team = []
        players_with_pieza = []
        pieza_distribution = []
        all_piezas_same_team = []
        muestra_ranks = []
        muestra_suits = []

        for i in range(num_simulations):
            # Generate a unique seed for each game based on the initial seed
            game_seed = None if seed is None else seed + i

            self.game.deal_cards(seed=game_seed)

            players_with_flower.append(self.game.count_players_with_flower())
            flower_distribution.append(self.game.get_flower_distribution())
            all_flowers_same_team.append(self.game.is_all_flowers_in_same_team())

            players_with_pieza.append(self.game.count_players_with_piezas())
            pieza_distribution.append(self.game.get_pieza_distribution())

            piezas_by_team = self.game.get_pieza_distribution()
            players_with_pieza_count = self.game.count_players_with_piezas()
            all_piezas_same = (
                any(
                    count == players_with_pieza_count
                    for count in piezas_by_team.values()
                )
                if players_with_pieza_count > 0
                else False
            )
            all_piezas_same_team.append(all_piezas_same)

            muestra = self.game.muestra
            if muestra is None:
                raise RuntimeError(
                    "deal_cards() must be called before reading its muestra"
                )
            muestra_ranks.append(muestra.rank.value)
            muestra_suits.append(muestra.suit.value)

        return SimulationResult(
            total_games=len(players_with_flower),
            players_with_flower=players_with_flower,
            flower_distribution=flower_distribution,
            all_flowers_same_team=all_flowers_same_team,
            players_with_pieza=players_with_pieza,
            pieza_distribution=pieza_distribution,
            all_piezas_same_team=all_piezas_same_team,
            muestra_ranks=muestra_ranks,
            muestra_suits=muestra_suits,
        )

    # Fixed version of run_simulations_parallel in simulator.py
    def run_simulations_parallel(
        self,
        num_simulations: int,
        num_workers: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> SimulationResult:
        """Run simulations in parallel using multiprocessing."""
        import multiprocessing as mp

        # Use CPU count if workers not specified
        if num_workers is None:
            num_workers = mp.cpu_count()

        # Divide simulations among workers
        sims_per_worker = [num_simulations // num_workers] * num_workers
        # Distribute remainder
        for i in range(num_simulations % num_workers):
            sims_per_worker[i] += 1

        # Set up seeds for each worker to ensure reproducibility
        worker_seeds: List[Optional[int]]
        if seed is not None:
            worker_seeds = [seed + i * 1000 for i in range(num_workers)]
        else:
            worker_seeds = [None] * num_workers

        # Prepare arguments for each worker
        args = [
            (sims, seed, self.game.num_players_per_team, self.game.num_teams)
            for sims, seed in zip(sims_per_worker, worker_seeds, strict=False)
        ]

        # Run simulations in parallel
        with mp.Pool(num_workers) as pool:
            results = pool.starmap(worker_function, args)

        # Combine results
        combined: Dict[str, List[Any]] = {
            "players_with_flower": [],
            "flower_distribution": [],
            "all_flowers_same_team": [],
            "players_with_pieza": [],
            "pieza_distribution": [],
            "all_piezas_same_team": [],
            "muestra_ranks": [],
            "muestra_suits": [],
        }

        for result in results:
            # Explicit per-key extends (not a loop over string keys): result
            # is a TypedDict, which only supports literal-key subscripting -
            # a dynamic str key isn't statically checkable against it.
            combined["players_with_flower"].extend(result["players_with_flower"])
            combined["flower_distribution"].extend(result["flower_distribution"])
            combined["all_flowers_same_team"].extend(result["all_flowers_same_team"])
            combined["players_with_pieza"].extend(result["players_with_pieza"])
            combined["pieza_distribution"].extend(result["pieza_distribution"])
            combined["all_piezas_same_team"].extend(result["all_piezas_same_team"])
            combined["muestra_ranks"].extend(result["muestra_ranks"])
            combined["muestra_suits"].extend(result["muestra_suits"])

        return SimulationResult(
            total_games=sum(sims_per_worker),
            players_with_flower=combined["players_with_flower"],
            flower_distribution=combined["flower_distribution"],
            all_flowers_same_team=combined["all_flowers_same_team"],
            players_with_pieza=combined["players_with_pieza"],
            pieza_distribution=combined["pieza_distribution"],
            all_piezas_same_team=combined["all_piezas_same_team"],
            muestra_ranks=combined["muestra_ranks"],
            muestra_suits=combined["muestra_suits"],
        )
