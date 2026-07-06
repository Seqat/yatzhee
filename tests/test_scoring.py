"""Tests for the scoring module."""

from src.yahtzee.scoring import SCORE_FUNCS


class TestUpperCategories:
    """Test upper section scoring (Ones through Sixes)."""

    def test_ones(self):
        assert SCORE_FUNCS["Ones"]([1, 1, 3, 4, 5]) == 2
        assert SCORE_FUNCS["Ones"]([2, 2, 2, 2, 2]) == 0
        assert SCORE_FUNCS["Ones"]([1, 1, 1, 1, 1]) == 5

    def test_twos(self):
        assert SCORE_FUNCS["Twos"]([2, 2, 2, 4, 5]) == 6
        assert SCORE_FUNCS["Twos"]([1, 1, 1, 1, 1]) == 0
        assert SCORE_FUNCS["Twos"]([2, 2, 2, 2, 2]) == 10

    def test_threes(self):
        assert SCORE_FUNCS["Threes"]([3, 3, 1, 4, 5]) == 6
        assert SCORE_FUNCS["Threes"]([3, 3, 3, 3, 3]) == 15
        assert SCORE_FUNCS["Threes"]([1, 1, 1, 1, 1]) == 0

    def test_fours(self):
        assert SCORE_FUNCS["Fours"]([4, 4, 4, 4, 5]) == 16
        assert SCORE_FUNCS["Fours"]([1, 1, 1, 1, 1]) == 0

    def test_fives(self):
        assert SCORE_FUNCS["Fives"]([5, 5, 1, 2, 3]) == 10
        assert SCORE_FUNCS["Fives"]([5, 5, 5, 5, 5]) == 25

    def test_sixes(self):
        assert SCORE_FUNCS["Sixes"]([6, 6, 6, 1, 2]) == 18
        assert SCORE_FUNCS["Sixes"]([1, 1, 1, 1, 1]) == 0


class TestThreeOfAKind:
    """Test Three of a Kind category."""

    def test_three_of_a_kind_valid(self):
        assert SCORE_FUNCS["Three of a Kind"]([3, 3, 3, 2, 5]) == 16
        assert SCORE_FUNCS["Three of a Kind"]([2, 2, 2, 2, 5]) == 13

    def test_three_of_a_kind_four_of_a_kind(self):
        # Four of a kind also scores as three of a kind
        assert SCORE_FUNCS["Three of a Kind"]([1, 1, 1, 1, 5]) == 9

    def test_three_of_a_kind_yahtzee(self):
        # Yahtzee also scores as three of a kind
        assert SCORE_FUNCS["Three of a Kind"]([4, 4, 4, 4, 4]) == 20

    def test_three_of_a_kind_invalid(self):
        # Less than three of a kind
        assert SCORE_FUNCS["Three of a Kind"]([1, 1, 2, 3, 4]) == 0
        assert SCORE_FUNCS["Three of a Kind"]([1, 2, 3, 4, 5]) == 0


class TestFourOfAKind:
    """Test Four of a Kind category."""

    def test_four_of_a_kind_valid(self):
        assert SCORE_FUNCS["Four of a Kind"]([2, 2, 2, 2, 5]) == 13
        assert SCORE_FUNCS["Four of a Kind"]([6, 6, 6, 6, 1]) == 25

    def test_four_of_a_kind_yahtzee(self):
        # Yahtzee also scores as four of a kind
        assert SCORE_FUNCS["Four of a Kind"]([3, 3, 3, 3, 3]) == 15

    def test_four_of_a_kind_invalid(self):
        # Three of a kind should not score
        assert SCORE_FUNCS["Four of a Kind"]([1, 1, 1, 2, 3]) == 0
        assert SCORE_FUNCS["Four of a Kind"]([1, 2, 3, 4, 5]) == 0


class TestFullHouse:
    """Test Full House category."""

    def test_full_house_valid(self):
        assert SCORE_FUNCS["Full House"]([3, 3, 3, 5, 5]) == 25
        assert SCORE_FUNCS["Full House"]([1, 1, 2, 2, 2]) == 25
        assert SCORE_FUNCS["Full House"]([6, 6, 4, 4, 4]) == 25

    def test_full_house_invalid_three_of_a_kind(self):
        # Three of a kind without pair
        assert SCORE_FUNCS["Full House"]([1, 1, 1, 2, 3]) == 0

    def test_full_house_invalid_pair(self):
        # Just a pair
        assert SCORE_FUNCS["Full House"]([1, 1, 2, 3, 4]) == 0

    def test_full_house_invalid_two_pairs(self):
        # Two pairs (but not full house)
        assert SCORE_FUNCS["Full House"]([1, 1, 2, 2, 3]) == 0

    def test_full_house_invalid_yahtzee(self):
        # Yahtzee does not count as full house
        assert SCORE_FUNCS["Full House"]([5, 5, 5, 5, 5]) == 0


class TestStraights:
    """Test Small and Large Straight categories."""

    def test_small_straight_valid(self):
        assert SCORE_FUNCS["Small Straight"]([1, 2, 3, 4, 5]) == 30
        assert SCORE_FUNCS["Small Straight"]([2, 3, 4, 5, 6]) == 30
        assert SCORE_FUNCS["Small Straight"]([1, 2, 3, 4, 1]) == 30
        assert SCORE_FUNCS["Small Straight"]([6, 5, 4, 3, 2]) == 30

    def test_small_straight_invalid(self):
        assert SCORE_FUNCS["Small Straight"]([1, 1, 3, 4, 5]) == 0
        assert SCORE_FUNCS["Small Straight"]([1, 2, 2, 4, 5]) == 0
        assert SCORE_FUNCS["Small Straight"]([1, 2, 4, 5, 6]) == 0

    def test_large_straight_valid(self):
        assert SCORE_FUNCS["Large Straight"]([1, 2, 3, 4, 5]) == 40
        assert SCORE_FUNCS["Large Straight"]([2, 3, 4, 5, 6]) == 40

    def test_large_straight_invalid(self):
        assert SCORE_FUNCS["Large Straight"]([1, 2, 3, 4, 4]) == 0
        assert SCORE_FUNCS["Large Straight"]([1, 2, 3, 5, 6]) == 0
        assert SCORE_FUNCS["Large Straight"]([1, 3, 4, 5, 6]) == 0


class TestYahtzee:
    """Test Yahtzee category (all five dice the same)."""

    def test_yahtzee_valid(self):
        assert SCORE_FUNCS["Yahtzee"]([1, 1, 1, 1, 1]) == 50
        assert SCORE_FUNCS["Yahtzee"]([6, 6, 6, 6, 6]) == 50
        assert SCORE_FUNCS["Yahtzee"]([3, 3, 3, 3, 3]) == 50

    def test_yahtzee_invalid(self):
        assert SCORE_FUNCS["Yahtzee"]([1, 1, 1, 1, 2]) == 0
        assert SCORE_FUNCS["Yahtzee"]([1, 2, 3, 4, 5]) == 0


class TestChance:
    """Test Chance category (sum of all dice, no restrictions)."""

    def test_chance(self):
        assert SCORE_FUNCS["Chance"]([1, 2, 3, 4, 5]) == 15
        assert SCORE_FUNCS["Chance"]([6, 6, 6, 6, 6]) == 30
        assert SCORE_FUNCS["Chance"]([1, 1, 1, 1, 1]) == 5
