# summle-solver

This is a simple script to find solutions to [Summle challenges](https://summle.net/).

## Usage (no installation)

`summle-solver` has no runtime dependencies. The easiest way to use it is to run the code directly with Python 3.10+:

```bash
python src/summle.py <target number> <list of input numbers>
python src/summle.py [medium|hard|extreme]  # fetch daily puzzle
python src/summle.py -i <target number> <list of input numbers>  # interactive mode: hints and simple calculator
```

## Installation

Install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

For development (includes pytest, mypy, ruff):

```bash
uv sync --extra dev
```

**Note:** This project uses PyPy for better performance. If you don't have PyPy installed:

```bash
uv python install pypy@3.10
uv sync
```

Or use CPython instead:

```bash
uv python pin 3.11  # or any Python 3.10+
uv sync
```

## Usage

To solve a puzzle:

```bash
uv run summle <target number> <list of input numbers>
```

To solve the daily summle problem:

```bash
uv run summle [medium|hard|extreme]
```

Interactive mode (shows hint, command-line calculator, prime decomposition):

```bash
uv run summle -i <target number> <list of input numbers>
uv run summle -i [medium|hard|extreme]
```

## Development

Run tests:

```bash
uv run pytest
```

Run type checking:

```bash
uv run mypy src
```

Format code:

```bash
uv run ruff format
```

Lint code:

```bash
uv run ruff check
```

## TODO

- Clean up the solving logic:
  - remove duplicate solutions
  - delegate solution finding to something faster than Python
- improve interactive mode:
  - make prime decomposition a sub-action of the calculator, all the time
  - less clutter in the REPL
  - Reset puzzle values / fetch new puzzle in the interactive mode (add /commands à la Claude)
- fix mypy errors
