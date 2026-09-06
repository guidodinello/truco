# Truco Uruguayo Probability Simulator

A Python package for simulating and analyzing probabilities in the card game Truco Uruguayo.

## Overview

This simulator allows you to run thousands of simulated Truco Uruguayo games to analyze the probability distribution of various game events, with a focus on "flowers" (three cards of the same suit) and "piezas" (special cards based on the muestra).

Key features:

- Simulate any number of Truco Uruguayo games
- Analyze the probability of players having flowers and piezas
- Visualize the distribution of special combinations across teams
- Calculate conditional probabilities for various game scenarios
- Analyze the impact of the "muestra" (trump card) on game outcomes

## Installation

Requirements:
- Python 3.13+
- uv (for dependency management)

```bash
# Clone the repository
git clone https://github.com/yourusername/truco.git
cd truco

# Setup the project (creates virtual environment and installs dependencies)
chmod +x setup.sh
./setup.sh
```

## Usage

### Command Line Interface

```bash
# Run 10,000 simulations with default settings
python -m truco.main

# Run 50,000 simulations with 3 players per team and generate visualizations
python -m truco.main -n 50000 -p 3 -v

# Use a specific random seed for reproducibility
python -m truco.main -n 10000 -s 42

# Generate detailed statistics
python -m truco.main -n 10000 -d

# Output results in JSON format
python -m truco.main -n 10000 -j

# Save visualizations to a specific directory
python -m truco.main -n 10000 -v -o ./my_plots
```

### Python API

You can also use the simulator programmatically:

```python
from truco.simulation.simulator import Simulator
from truco.analysis.statistics import StatisticsAnalyzer
from truco.visualization.visualizer import Visualizer

# Run simulations
simulator = Simulator(players_per_team=3, num_teams=2)
results = simulator.run_simulations(num_simulations=10000, seed=None)

# Analyze results
analyzer = StatisticsAnalyzer(results)
flower_stats = analyzer.calculate_flower_stats()
pieza_stats = analyzer.calculate_pieza_stats()
joint_stats = analyzer.calculate_combined_stats()

# Generate visualizations
visualizer = Visualizer(results)
visualizer.plot_flower_distribution(save_path="flower_distribution.png")
visualizer.plot_pieza_distribution(save_path="pieza_distribution.png")
```

## Truco Uruguayo Rules

Truco Uruguayo is a popular card game in Uruguay and parts of Argentina. It's played with a 40-card Spanish deck, with the following key features:

- Usually played with 4 or 6 players (2 or 3 per team)
- Each player receives 3 cards per hand
- A "flower" occurs when a player has all three cards of the same suit
- A "muestra" (trump) card is revealed at the start of each hand
- Special cards called "piezas" have higher values when they match the suit of the muestra
- The "piezas" in order of value are: 2, 4, 5, 10, 11 of the muestra suit
- If the muestra itself is one of these cards, the 12 of the same suit takes a special role

This simulator focuses on analyzing the probabilities related to these special combinations in the game.

## Visualization Examples

The simulator can generate a variety of visualizations:

1. **Flower Distribution**: Probability of different numbers of players having flowers
2. **Pieza Distribution**: Probability of different numbers of players having piezas
3. **Team Advantage**: Distribution of flower/pieza advantages between teams
4. **Conditional Probabilities**: Probability of all flowers/piezas being in the same team
5. **Muestra Distribution**: Analysis of the muestra card distribution
6. **Joint Probabilities**: Relationship between flowers and piezas in games

## Project Structure

```
src/
└── truco/              # Main package
    ├── __init__.py
    ├── main.py         # Entry point
    ├── domain/         # Domain model
    │   ├── __init__.py
    │   ├── card.py     # Card representation
    │   ├── deck.py     # Deck operations
    │   ├── hand.py     # Player's hand
    │   ├── player.py   # Player representation
    │   ├── team.py     # Team representation
    │   └── game.py     # Game rules and logic
    ├── simulation/     # Simulation engine
    │   ├── __init__.py
    │   └── simulator.py
    ├── analysis/       # Analysis tools
    │   ├── __init__.py
    │   └── statistics.py
    ├── visualization/  # Visualization tools
    │   ├── __init__.py
    │   └── visualizer.py
    └── interface/      # User interfaces
        ├── __init__.py
        └── cli.py
```

## Development

This project uses:
- `pre-commit` for managing git hooks
- `ruff` for linting and formatting
- `mypy` for static type checking

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

## License

[MIT License](LICENSE)
