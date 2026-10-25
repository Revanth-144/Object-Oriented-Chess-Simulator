# Object-Oriented Chess Simulator

A desktop chess game built in Python with Pygame. The project combines a chess rules engine, a graphical board, and a lightweight chess AI to provide a playable local chess experience.

## Overview

This repository contains a complete object-oriented chess implementation that models the board, legal move generation, special moves, check/checkmate detection, and user interaction through a graphical interface. The engine is intentionally simple and educational: it focuses on core chess logic and an AI opponent based on move evaluation and search rather than a full engine like Stockfish.

The project is centered around three main files:

- [ChessEngine.py](ChessEngine.py): the chess rules engine and board state logic
- [ChessMain.py](ChessMain.py): the Pygame UI, event loop, and rendering layer
- [SmartMoveFinder.py](SmartMoveFinder.py): the AI move selection logic and evaluation heuristics

## Features

- 8x8 chess board with standard piece movement
- Legal move validation and move generation
- Check detection, checkmate, and stalemate handling
- Special move support for castling and en passant capture
- Pawn promotion to a queen by default
- Move log and board state tracking
- Undo move support with `z`
- Reset board support with `r`
- Human-vs-human or human-vs-AI behavior controlled in code
- AI move generation using minimax-style search with alpha-beta pruning and position scoring
- Graphical chessboard using Pygame assets from [Images/](Images/)

## Tech Stack

- Python 3
- Pygame for rendering and input handling
- Multiprocessing for asynchronous AI move computation
- Standard library modules such as `random`

## Project Structure

```text
.
├── ChessEngine.py          # Core chess rules and board logic
├── ChessMain.py            # Game loop, rendering, input handling, and UI
├── SmartMoveFinder.py      # Chess AI move search and evaluation
├── Images/                 # Chess piece sprite PNG files
│   ├── bB.png
│   ├── bK.png
│   ├── bN.png
│   ├── bQ.png
│   ├── bR.png
│   ├── bp.png
│   ├── wB.png
│   ├── wK.png
│   ├── wN.png
│   ├── wQ.png
│   ├── wR.png
│   └── wp.png
├── README.md               # Project documentation
├── __pycache__/            # Generated Python cache files
└── .git/                   # Git metadata
```

### Key Files

- [ChessEngine.py](ChessEngine.py): stores the board state, validates legal moves, handles check states, castling rights, en passant tracking, and move history.
- [ChessMain.py](ChessMain.py): initializes the Pygame window, loads piece images, draws the board, handles mouse and keyboard input, runs the game loop, and triggers the AI turn logic.
- [SmartMoveFinder.py](SmartMoveFinder.py): implements board evaluation and move search using heuristic scoring and alpha-beta pruning.
- [Images/](Images/): contains the visual chess piece assets used by the board renderer.

## Prerequisites

Before running the project, make sure you have:

- Python 3 installed
- A desktop environment capable of running Pygame
- `pip` available to install Python dependencies
- The repository checked out locally

This project does not declare a pinned Python version or a `requirements.txt` file, so the repository is best used with a standard Python 3 environment.

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/Revanth-144/Object-Oriented-Chess-Simulator.git
cd Object-Oriented-Chess-Simulator
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the dependency:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pygame
```

4. Start the game:

```bash
python3 ChessMain.py
```

## Environment Variables

This project does not currently use a `.env` file, environment variables, API keys, database configuration, or external cloud services.

```env
# No environment variables are required.
```

| Variable | Required | Description |
| --- | --- | --- |
| None | No | The project is fully local and does not read secrets or external configuration at runtime. |

## Usage

After launching the game, the board appears in a Pygame window. The application uses mouse clicks to select a piece and choose a destination square.

### Controls

- Click a piece, then click the destination square to move it.
- Press `z` to undo the last move.
- Press `r` to reset the board.
- Close the window to quit the application.

### AI Behavior

The current implementation contains a basic AI and uses multiprocessing to evaluate moves in a separate process. In the current code, the flags `playerOne` and `playerTwo` in [ChessMain.py](ChessMain.py) control whether each side is a human or AI.

```python
playerOne = False
playerTwo = False
```

This means the game currently defaults to AI-controlled turns for both sides unless those values are edited.

## Examples / Screenshots

This repository does not include screenshots or a demo video in the project folder, so the examples below reflect the actual behavior implemented in the code.

### Example move input

A valid move is selected by mouse click. The game prints the move notation to the console as it is processed, for example:

```text
e2e4
```

### Example startup output

Running the game in a headless environment produced output similar to:

```text
AI is thinking...
AI has made a move.
AI is thinking...
```

## Architecture / Workflow

The application follows a straightforward object-oriented design:

1. [ChessEngine.py](ChessEngine.py) holds the board state and exposes operations like `makeMove()`, `undoMove()`, and `getValidMoves()`.
2. Move generation is based on the piece type and board position, with checks for validity and special rules.
3. [ChessMain.py](ChessMain.py) listens for mouse and keyboard input, updates the board state, and renders the current game state on screen.
4. [SmartMoveFinder.py](SmartMoveFinder.py) evaluates board positions and searches for the best move using a heuristic and alpha-beta pruning.
5. The game loop repeatedly draws the board and updates state as players make moves.

## Testing

No automated test suite is configured in this repository. There are no `pytest` or `unittest` files present, and no `requirements.txt` or project-specific test command is defined.

A basic manual smoke test can still be run from the project root:

```bash
cd Object-Oriented-Chess-Simulator
SDL_VIDEODRIVER=dummy python3 - <<'PY'
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import ChessEngine

gs = ChessEngine.GameState()
print(len(gs.getValidMoves()))
PY
```

This confirms that the board initializes and the engine can generate legal moves.

## Sample Input and Output

### Example operation

```bash
python3 ChessMain.py
```

Expected behavior:

- A chessboard is displayed.
- Valid moves are generated as you click pieces.
- The game can display current move notation in the terminal output.
- The AI may move automatically depending on the `playerOne` and `playerTwo` settings.

## Known Limitations

- There is no graphical menu, settings screen, or game configuration UI.
- The AI is heuristic-based and is not a strong chess engine comparable with top-tier engines.
- The project does not include automated tests or continuous integration.
- The game defaults to AI-controlled turns unless the booleans in [ChessMain.py](ChessMain.py) are edited.
- There is no packaged executable, installer, or cross-platform release artifact.

## Future Improvements

Possible next steps for this project include:

- Add a proper human-vs-human / human-vs-AI selection screen
- Add difficulty levels for the AI
- Improve move evaluation with better positional heuristics and deeper search
- Add sound effects and richer UI polish
- Add more complete chess notation and move history features
- Add automated tests for core engine behavior

---

This project is useful as a learning tool or a starting point for a more advanced chess application. It demonstrates how chess rules, move generation, graphics, and search-based AI can be organized in a clean object-oriented Python project.
