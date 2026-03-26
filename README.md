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
git clone https://github.com/<your-username>/yahtzee.git
cd yahtzee
```

### 2. Create a virtual environment (optional)

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
pip install -r requirements.txt
```

### 4. Run the game

```bash
python yahtzee.py
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

- **Language:** Python 3
- **GUI Framework:** Tkinter (standard library)
- **Dependencies:** None — uses only Python standard library modules

## 📁 Project Structure

```
yahtzee/
├── yahtzee.py          # Main game (all logic + GUI)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
