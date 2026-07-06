"""Game state and turn flow for a 2-player Yahtzee game."""

import random

from .constants import (
    ALL_CATS, DICE_COUNT, MAX_ROLLS, TOTAL_ROUNDS,
    UPPER_BONUS, UPPER_BONUS_THRESHOLD, UPPER_CATS,
)
from .scoring import SCORE_FUNCS


class YahtzeeGame:
    """Manages state for a 2-player Yahtzee game."""

    def __init__(self):
        self.player_names = ["Player 1", "Player 2"]
        self.reset()

    def reset(self):
        self.dice       = [1] * DICE_COUNT
        self.held       = [False] * DICE_COUNT
        self.rolls_left = MAX_ROLLS
        self.scores     = [
            {cat: None for cat in ALL_CATS},
            {cat: None for cat in ALL_CATS},
        ]
        self.rounds     = [1, 1]          # per-player round counter
        self.current    = 0               # whose turn (0 or 1)
        self.game_over  = False

    def roll(self):
        if self.rolls_left <= 0 or self.game_over:
            return
        for i in range(DICE_COUNT):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)
        self.rolls_left -= 1

    def potential(self, cat):
        return SCORE_FUNCS[cat](self.dice)

    def assign(self, cat):
        p = self.current
        if self.scores[p][cat] is not None or self.rolls_left == MAX_ROLLS:
            return False
        self.scores[p][cat] = self.potential(cat)
        self.rounds[p] += 1
        # Reset dice state for next turn
        self.held       = [False] * DICE_COUNT
        self.rolls_left = MAX_ROLLS
        self.dice       = [1] * DICE_COUNT
        # Switch player
        self.current = 1 - p
        # Check if game is over (both players completed all rounds)
        if self.rounds[0] > TOTAL_ROUNDS and self.rounds[1] > TOTAL_ROUNDS:
            self.game_over = True
        return True

    def _player_stats(self, p):
        upper_sub = sum(
            s for c, s in self.scores[p].items()
            if c in UPPER_CATS and s is not None
        )
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
