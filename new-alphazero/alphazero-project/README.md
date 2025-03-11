# AlphaZero Project

This project implements the AlphaZero algorithm for playing board games using Monte Carlo Tree Search (MCTS) and deep learning.

## Project Structure

- `src/game.py`: Contains the game logic, including state management, rule enforcement, and win/loss determination.
- `src/MCTS.py`: Implements the Monte Carlo Tree Search (MCTS) algorithm, with methods for node selection, expansion, simulation, and backpropagation to choose optimal moves based on the game state.
- `src/network.py`: Implements the neural network architecture for AlphaZero, including policy and value networks for training and inference.
- `src/utils.py`: Provides utility functions for data preprocessing, result saving, and logging, used across other modules.
- `requirements.txt`: Lists the project dependencies. Install them using `pip install -r requirements.txt`.
- `setup.py`: Contains the setup script for the project, defining package metadata and dependencies for installation.
- `README.md`: Documentation for the project, including an overview, installation instructions, usage, and license information.

## Installation

To install the project, clone the repository and navigate to the project directory. Then, run:

```
pip install -r requirements.txt
```

## Usage

To use the AlphaZero implementation, you can run the main script in the `src` directory. Ensure that you have the necessary dependencies installed.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.