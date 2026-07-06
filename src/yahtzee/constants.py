"""Game rules constants and static display data."""

DICE_COUNT = 5
MAX_ROLLS = 3
TOTAL_ROUNDS = 13
UPPER_BONUS_THRESHOLD = 63
UPPER_BONUS = 35

UPPER_CATS = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
LOWER_CATS = [
    "Three of a Kind",
    "Four of a Kind",
    "Full House",
    "Small Straight",
    "Large Straight",
    "Yahtzee",
    "Chance",
]
ALL_CATS = UPPER_CATS + LOWER_CATS

# Die face dot positions (normalized 0-1)
DOT_POSITIONS = {
    1: [(0.5, 0.5)],
    2: [(0.28, 0.28), (0.72, 0.72)],
    3: [(0.28, 0.28), (0.5, 0.5), (0.72, 0.72)],
    4: [(0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72)],
    5: [(0.28, 0.28), (0.72, 0.28), (0.5, 0.5), (0.28, 0.72), (0.72, 0.72)],
    6: [(0.28, 0.22), (0.72, 0.22), (0.28, 0.5), (0.72, 0.5), (0.28, 0.78), (0.72, 0.78)],
}

# Category descriptions (for tooltips)
CATEGORY_HINTS = {
    "Ones": "Sum of all dice showing 1.\nExample: [1,1,3,4,5] → 2 pts",
    "Twos": "Sum of all dice showing 2.\nExample: [2,2,2,4,5] → 6 pts",
    "Threes": "Sum of all dice showing 3.\nExample: [3,3,1,4,5] → 6 pts",
    "Fours": "Sum of all dice showing 4.\nExample: [4,4,4,4,5] → 16 pts",
    "Fives": "Sum of all dice showing 5.\nExample: [5,5,1,2,3] → 10 pts",
    "Sixes": "Sum of all dice showing 6.\nExample: [6,6,6,1,2] → 18 pts",
    "Three of a Kind": "At least three dice the same.\nScore = sum of ALL dice.\nExample: [3,3,3,2,5] → 16 pts",
    "Four of a Kind": "At least four dice the same.\nScore = sum of ALL dice.\nExample: [2,2,2,2,5] → 13 pts",
    "Full House": "Three of one kind + two of another.\nAlways scores 25 pts.\nExample: [3,3,3,5,5] → 25 pts",
    "Small Straight": "Four sequential dice (e.g. 1-2-3-4).\nAlways scores 30 pts.",
    "Large Straight": "Five sequential dice (e.g. 1-2-3-4-5).\nAlways scores 40 pts.",
    "Yahtzee": "All five dice the same!\nScores 50 pts.\nExample: [4,4,4,4,4] → 50 pts",
    "Chance": "No requirements — sum of all dice.\nUse as a fallback for bad rolls.",
}
