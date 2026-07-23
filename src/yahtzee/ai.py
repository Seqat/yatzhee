"""AI opponent logic ('easy' or 'hard' difficulty)."""

import random
from collections import Counter

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
            # Prefer holds that actually keep some dice
            if score > best_score or (score == best_score and sum(hold) > sum(best_hold)):
                best_score = score
                best_hold = hold

        game.held = best_hold

    def _best_hold_for_category(self, cat, dice):
        """Find the best hold pattern for a given category."""
        n = len(dice)

        # Special handling for upper section - hold matching dice
        if cat in UPPER_CATS:
            target = UPPER_CATS.index(cat) + 1
            hold = [d == target for d in dice]
            return SCORE_FUNCS[cat](dice), hold

        counts = Counter(dice)
        most_common_val, most_common_count = counts.most_common(1)[0]

        if cat == "Three of a Kind":
            if most_common_count >= 3:
                return sum(dice), [True] * n
            return 0, [d == most_common_val for d in dice]

        elif cat == "Four of a Kind":
            if most_common_count >= 4:
                return sum(dice), [True] * n
            return 0, [d == most_common_val for d in dice]

        elif cat == "Yahtzee":
            if most_common_count == 5:
                return 50, [True] * n
            return 0, [d == most_common_val for d in dice]

        elif cat == "Full House":
            vals = sorted(counts.values())
            if vals == [2, 3]:
                return 25, [True] * n
            if most_common_count >= 3:
                held = [False] * n
                count = 0
                for i, d in enumerate(dice):
                    if d == most_common_val and count < 3:
                        held[i] = True
                        count += 1
                for val, cnt in counts.items():
                    if val != most_common_val and cnt >= 2:
                        for i, d in enumerate(dice):
                            if d == val and held[i] is False:
                                held[i] = True
                        break
                return 0, held
            return 0, [d == most_common_val for d in dice]

        elif cat in ("Small Straight", "Large Straight"):
            unique_sorted = sorted(set(dice))
            held = [False] * n
            for i, d in enumerate(dice):
                if d in unique_sorted:
                    held[i] = True
            return 0, held

        elif cat == "Chance":
            # Hold all dice for chance - we want to maximize sum
            return sum(dice), [True] * n

        return 0, [False] * n

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
