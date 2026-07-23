"""Pure scoring functions for each Yahtzee category."""

from collections import Counter


def _upper(n):
    return lambda dice: sum(d for d in dice if d == n)


def _three_kind(dice):
    counts = Counter(dice)
    return sum(dice) if any(v >= 3 for v in counts.values()) else 0


def _four_kind(dice):
    counts = Counter(dice)
    return sum(dice) if any(v >= 4 for v in counts.values()) else 0


def _full_house(dice):
    counts = Counter(dice)
    vals = sorted(counts.values())
    return 25 if vals == [2, 3] else 0


def _small_straight(dice):
    s = set(dice)
    return 30 if any(run.issubset(s) for run in [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]) else 0


def _large_straight(dice):
    s = set(dice)
    return 40 if s in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0


def _yahtzee(dice):
    first = dice[0]
    return 50 if all(d == first for d in dice) else 0


def _chance(dice):
    return sum(dice)


SCORE_FUNCS = {
    "Ones": _upper(1),
    "Twos": _upper(2),
    "Threes": _upper(3),
    "Fours": _upper(4),
    "Fives": _upper(5),
    "Sixes": _upper(6),
    "Three of a Kind": _three_kind,
    "Four of a Kind": _four_kind,
    "Full House": _full_house,
    "Small Straight": _small_straight,
    "Large Straight": _large_straight,
    "Yahtzee": _yahtzee,
    "Chance": _chance,
}
