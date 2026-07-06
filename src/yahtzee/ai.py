"""AI opponent logic ('easy' or 'hard' difficulty)."""

import random
from collections import Counter
from itertools import combinations

from .constants import ALL_CATS, DICE_COUNT, UPPER_CATS
from .scoring import SCORE_FUNCS


class AIPlayer:
    """AI opponent with 'easy' or 'hard' difficulty."""

    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty  # "easy" or "hard"

    # ── Easy AI ───────────────────────────────────────────────────────────────
    def _easy_choose_holds(self, game):
        """Easy AI: don't hold anything — just re-roll all dice."""
        game.held = [False] * DICE_COUNT

    def _easy_choose_category(self, game):
        """Easy AI: pick a random available category."""
        p = game.current
        available = [c for c in ALL_CATS if game.scores[p][c] is None]
        return random.choice(available) if available else None

    # ── Hard AI ───────────────────────────────────────────────────────────────
    def _hard_choose_holds(self, game):
        """Hard AI: evaluate which dice to hold for the best expected score."""
        p = game.current
        available = [c for c in ALL_CATS if game.scores[p][c] is None]
        dice = list(game.dice)

        best_score = -1
        best_hold = [False] * DICE_COUNT

        # For each available category, figure out which dice to keep
        for cat in available:
            score, hold = self._best_hold_for_category(cat, dice)
            if score > best_score:
                best_score = score
                best_hold = hold

        game.held = best_hold

    def _best_hold_for_category(self, cat, dice):
        """Find the best hold pattern for a given category."""
        n = len(dice)
        best_score = SCORE_FUNCS[cat](dice)
        best_hold = [True] * n  # default: hold all (current score is best)

        # Try all possible hold subsets (2^5 = 32 combinations)
        for num_held in range(n + 1):
            for held_indices in combinations(range(n), num_held):
                hold = [False] * n
                for idx in held_indices:
                    hold[idx] = True
                # Score if we hold these dice (approximate: just use current)
                test_dice = [dice[i] for i in range(n) if hold[i]]
                if len(test_dice) == n:
                    score = SCORE_FUNCS[cat](dice)
                else:
                    score = SCORE_FUNCS[cat](dice)  # current dice for eval

                # For upper section, hold matching dice
                if cat in UPPER_CATS:
                    target = UPPER_CATS.index(cat) + 1
                    hold = [d == target for d in dice]
                    score = SCORE_FUNCS[cat](dice)
                    return score, hold

                if score > best_score:
                    best_score = score
                    best_hold = hold

        # Special heuristics for lower section
        counts = Counter(dice)
        most_common_val, most_common_count = counts.most_common(1)[0]

        if cat in ("Three of a Kind", "Four of a Kind", "Yahtzee"):
            # Hold the most frequent die value
            best_hold = [d == most_common_val for d in dice]
        elif cat == "Full House":
            if most_common_count >= 3:
                # Hold three of the most common, and a pair if exists
                held = [False] * n
                count = 0
                for i, d in enumerate(dice):
                    if d == most_common_val and count < 3:
                        held[i] = True
                        count += 1
                # Try to hold a pair of another value
                for val, cnt in counts.items():
                    if val != most_common_val and cnt >= 2:
                        pair_count = 0
                        for i, d in enumerate(dice):
                            if d == val and pair_count < 2:
                                held[i] = True
                                pair_count += 1
                        break
                best_hold = held
            else:
                best_hold = [d == most_common_val for d in dice]
        elif cat in ("Small Straight", "Large Straight"):
            # Hold unique sequential dice
            seen = set()
            best_hold = [False] * n
            for i, d in enumerate(dice):
                if d not in seen:
                    best_hold[i] = True
                    seen.add(d)
        elif cat == "Chance":
            # Hold high-value dice (5s and 6s)
            best_hold = [d >= 5 for d in dice]

        return best_score, best_hold

    def _hard_choose_category(self, game):
        """Hard AI: pick the category that yields the highest score."""
        p = game.current
        available = [c for c in ALL_CATS if game.scores[p][c] is None]
        if not available:
            return None

        best_cat = None
        best_score = -1
        for cat in available:
            score = game.potential(cat)
            # Prefer scoring > 0; penalize wasting good categories with 0
            weight = score
            if score == 0:
                # Prefer wasting lower-value categories
                if cat in UPPER_CATS:
                    weight = -1  # slightly prefer wasting upper cats
                else:
                    weight = -10  # avoid wasting valuable lower cats
            if weight > best_score:
                best_score = weight
                best_cat = cat

        # If all scores are negative (all zeros), pick the least valuable to waste
        if best_score < 0:
            # Waste the least valuable category
            waste_priority = list(reversed(ALL_CATS))
            for cat in waste_priority:
                if cat in available:
                    return cat

        return best_cat

    def choose_holds(self, game):
        if self.difficulty == "easy":
            self._easy_choose_holds(game)
        else:
            self._hard_choose_holds(game)

    def choose_category(self, game):
        if self.difficulty == "easy":
            return self._easy_choose_category(game)
        else:
            return self._hard_choose_category(game)
