# 🎲 Yahtzee

A classic Yahtzee dice game built with Python and Tkinter, featuring a sleek dark-themed GUI, 2-player support, and AI opponents.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🎮 Multiple Game Modes**
  - **2 Players (Local)** — Play against a friend on the same computer
  - **vs AI (Easy)** — AI picks randomly, great for beginners
  - **vs AI (Hard)** — AI uses strategic heuristics to maximize score

- **🎨 Modern Dark UI** — Sleek dark theme with color-coded players and animated dice

- **💡 Category Tooltips** — Hover over any scoring category to see a description with examples

- **📊 Dual Scorecard** — Side-by-side score tracking for both players with upper section bonus tracking

## 📋 Requirements

- Python 3.8 or higher
- Tkinter (included with most Python installations)

#### Platform-specific Tkinter installation

| Platform | Command |
|---|---|
| **macOS** (Homebrew) | `brew install python-tk` |
| **Ubuntu / Debian** | `sudo apt install python3-tk` |
| **Fedora** | `sudo dnf install python3-tkinter` |
| **Arch Linux** | `sudo pacman -S tk` |
| **Windows** | Included by default with the [python.org](https://www.python.org/downloads/) installer |

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Seqat/yahtzee.git
cd yahtzee
```

### 2. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Run the game

```bash
yahtzee
```

**Alternative methods:**
- Using Python module: `python -m yahtzee`
- Using Make (macOS/Linux): `make run`

## 🛠️ Development

### Install with dev dependencies

```bash
pip install -e ".[dev]"
```

Or using Make:
```bash
make dev
```

### Running tests

```bash
pytest tests/ -v
```

Using Make:
```bash
make test          # Run tests
make test-cov      # Run tests with coverage report
```

### Code quality

```bash
ruff check src/ tests/     # Lint code
black --check src/ tests/  # Check formatting
black src/ tests/          # Format code
```

Using Make:
```bash
make lint          # Lint with ruff
make format-check  # Check formatting
make format        # Auto-format with black
```

### Project structure

```
yahtzee/
├── src/yahtzee/           # Main package
│   ├── __init__.py        # Entry point
│   ├── __main__.py        # CLI launcher
│   ├── constants.py       # Game constants and theme
│   ├── game.py            # Core game logic
│   ├── scoring.py         # Scoring functions
│   ├── ai.py              # AI opponent logic
│   ├── persistence.py     # High scores and settings
│   ├── settings.py        # User preferences
│   └── ui/                # Tkinter UI components
│       ├── app.py
│       ├── widgets.py
│       └── tooltip.py
├── tests/                 # Test suite (75+ tests)
│   ├── test_game.py
│   ├── test_scoring.py
│   ├── test_validation.py
│   └── test_persistence.py
├── pyproject.toml         # Package configuration
├── Makefile              # Development commands
└── README.md
```

### Test coverage

The project has comprehensive test coverage for:
- **Scoring logic** (24 tests) — All 13 categories with edge cases
- **Game flow** (22 tests) — Turn alternation, state management, bonuses
- **Validation** (16 tests) — Input validation and error reporting
- **Persistence** (13 tests) — High scores and settings storage

Run tests with coverage:
```bash
pytest tests/ --cov=src/yahtzee --cov-report=html
```

## 🎯 How to Play

1. **Choose a game mode** from the start screen
2. **Roll the dice** up to 3 times per turn — click dice to hold/release them between rolls
3. **Pick a scoring category** from the scorecard to lock in your score for that turn
4. After **13 rounds each**, the player with the highest total score wins!

### Scoring Categories

| Category | Description |
|---|---|
| **Ones – Sixes** | Sum of dice showing that number |
| **Three of a Kind** | At least 3 same dice → sum of all dice |
| **Four of a Kind** | At least 4 same dice → sum of all dice |
| **Full House** | 3 of one + 2 of another → 25 pts |
| **Small Straight** | 4 sequential dice → 30 pts |
| **Large Straight** | 5 sequential dice → 40 pts |
| **Yahtzee** | All 5 dice the same → 50 pts |
| **Chance** | Sum of all dice (no requirements) |

> **Upper Section Bonus:** Score 63+ in the upper section (Ones–Sixes) to earn a **+35 bonus**!

## 🛠 Tech Stack

- **Language:** Python 3.8+
- **GUI Framework:** Tkinter (standard library)
- **Testing:** Pytest with coverage
- **Linting:** Ruff
- **Formatting:** Black
- **CI/CD:** GitHub Actions
- **Dependencies:** None — uses only Python standard library modules

## 🔄 CI/CD

This project uses GitHub Actions to automatically:
- Run tests on all pushes and pull requests
- Test across Python 3.8, 3.9, 3.10, 3.11
- Test on macOS, Ubuntu, and Windows
- Check code formatting and linting
- Upload coverage reports

**Status badges:** (Add these to the top of README after setting up Actions)
```markdown
[![Tests](https://github.com/Seqat/yahtzee/actions/workflows/tests.yml/badge.svg)](https://github.com/Seqat/yahtzee/actions/workflows/tests.yml)
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and ensure tests pass:
   ```bash
   make test
   make lint
   make format
   ```
4. Commit with clear messages: `git commit -am "Add new feature"`
5. Push to your fork: `git push origin feature/my-feature`
6. Open a pull request

### Code style

- **Formatting:** Black (line length 100)
- **Linting:** Ruff (E, F, W, I rules)
- **Type hints:** Recommended for new code
- **Tests:** Required for new features

Run before committing:
```bash
make format lint test
```
