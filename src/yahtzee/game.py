"""Game state and turn flow for a 2-player Yahtzee game."""

import random

from .constants import (
    ALL_CATS,
    DICE_COUNT,
    MAX_ROLLS,
    TOTAL_ROUNDS,
    UPPER_BONUS,
    UPPER_BONUS_THRESHOLD,
    UPPER_CATS,
)
from .scoring import SCORE_FUNCS


class YahtzeeGame:
    """Manages state for a 2-player Yahtzee game."""

    def __init__(self):
        self.player_names = ["Player 1", "Player 2"]
        self.reset()

    def reset(self):
        self.dice = [1] * DICE_COUNT
        self.held = [False] * DICE_COUNT
        self.rolls_left = MAX_ROLLS
        self.scores = [
            {cat: None for cat in ALL_CATS},
            {cat: None for cat in ALL_CATS},
        ]
        self.rounds = [1, 1]  # per-player round counter
        self.current = 0  # whose turn (0 or 1)
        self.game_over = False

    def roll(self):
        """Roll unheld dice. Returns True if roll was successful, False otherwise."""
        if self.game_over:
            return False
        if self.rolls_left <= 0:
            return False
        for i in range(DICE_COUNT):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)
        self.rolls_left -= 1
        return True

    def potential(self, cat):
        return SCORE_FUNCS[cat](self.dice)

    def assign(self, cat):
        """
        Assign a category score for the current player.
        Returns (success, reason) tuple for better feedback.
        """
        p = self.current

        if self.game_over:
            return False, "Game is over"

        if cat not in ALL_CATS:
            return False, "Invalid category"

        if self.scores[p][cat] is not None:
            return False, "Category already scored"

        if self.rolls_left == MAX_ROLLS:
            return False, "Must roll before scoring"

        self.scores[p][cat] = self.potential(cat)
        self.rounds[p] += 1
        # Reset dice state for next turn
        self.held = [False] * DICE_COUNT
        self.rolls_left = MAX_ROLLS
        self.dice = [1] * DICE_COUNT
        # Switch player
        self.current = 1 - p
        # Check if game is over (both players completed all rounds)
        if self.rounds[0] > TOTAL_ROUNDS and self.rounds[1] > TOTAL_ROUNDS:
            self.game_over = True
        return True, "Score assigned"

    def _player_stats(self, p):
        upper_sub = sum(s for c, s in self.scores[p].items() if c in UPPER_CATS and s is not None)
        bonus = UPPER_BONUS if upper_sub >= UPPER_BONUS_THRESHOLD else 0
        total = sum(s for s in self.scores[p].values() if s is not None) + bonus
        return upper_sub, bonus, total

    def upper_subtotal(self, p):
        return self._player_stats(p)[0]

    def bonus(self, p):
        return self._player_stats(p)[1]

    def total(self, p):
        return self._player_stats(p)[2]

    @property
    def current_name(self):
        return self.player_names[self.current]

    def can_roll(self):
        """Check if the current player can roll."""
        return not self.game_over and self.rolls_left > 0

    def can_assign(self, cat):
        """Check if a category can be assigned without providing detailed feedback."""
        if self.game_over or self.rolls_left == MAX_ROLLS:
            return False
        if cat not in ALL_CATS:
            return False
        return self.scores[self.current][cat] is None

    def get_available_categories(self):
        """Get list of unscored categories for the current player."""
        p = self.current
        return [cat for cat in ALL_CATS if self.scores[p][cat] is None]

    def get_scores_summary(self):
        """Get a summary of current scores for both players."""
        return {
            "player_names": self.player_names,
            "scores": [self.scores[0].copy(), self.scores[1].copy()],
            "totals": [self.total(0), self.total(1)],
            "upper_subtotals": [self.upper_subtotal(0), self.upper_subtotal(1)],
            "bonuses": [self.bonus(0), self.bonus(1)],
        }
