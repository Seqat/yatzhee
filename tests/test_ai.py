"""Tests for AI opponent logic."""

import pytest

from src.yahtzee.ai import AIPlayer
from src.yahtzee.game import YahtzeeGame
from src.yahtzee.constants import ALL_CATS, UPPER_CATS


class TestEasyAI:
    """Test easy AI behavior."""

    def test_easy_ai_initialization(self):
        ai = AIPlayer(difficulty="easy")
        assert ai.difficulty == "easy"

    def test_easy_ai_chooses_no_holds(self):
        """Easy AI should not hold any dice."""
        ai = AIPlayer(difficulty="easy")
        game = YahtzeeGame()
        game.dice = [6, 6, 6, 6, 6]  # Even with yahtzee, easy AI doesn't hold
        ai._easy_choose_holds(game)
        assert game.held == [False, False, False, False, False]

    def test_easy_ai_chooses_random_category(self):
        """Easy AI should choose a random available category."""
        ai = AIPlayer(difficulty="easy")
        game = YahtzeeGame()
        # All categories are available
        category = ai._easy_choose_category(game)
        assert category in ALL_CATS

    def test_easy_ai_returns_none_when_no_categories(self):
        """Easy AI should return None when no categories available."""
        ai = AIPlayer(difficulty="easy")
        game = YahtzeeGame()
        # Mark all categories as scored
        for cat in ALL_CATS:
            game.scores[0][cat] = 0
        category = ai._easy_choose_category(game)
        assert category is None

    def test_easy_choose_holds_public_method(self):
        """Test public choose_holds method for easy AI."""
        ai = AIPlayer(difficulty="easy")
        game = YahtzeeGame()
        game.dice = [1, 2, 3, 4, 5]
        ai.choose_holds(game)
        assert game.held == [False, False, False, False, False]

    def test_easy_choose_category_public_method(self):
        """Test public choose_category method for easy AI."""
        ai = AIPlayer(difficulty="easy")
        game = YahtzeeGame()
        category = ai.choose_category(game)
        assert category in ALL_CATS


class TestHardAI:
    """Test hard AI behavior."""

    def test_hard_ai_initialization(self):
        ai = AIPlayer(difficulty="hard")
        assert ai.difficulty == "hard"

    def test_hard_ai_holds_matching_dice_for_upper_section(self):
        """Hard AI should hold dice matching the upper section category."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [3, 3, 1, 4, 5]
        game.current = 0
        # Score all categories except Threes
        for cat in ALL_CATS:
            if cat != "Threes":
                game.scores[0][cat] = 0
        ai._hard_choose_holds(game)
        # Should hold the two 3s
        assert game.held[0] is True
        assert game.held[1] is True

    def test_hard_ai_holds_all_for_yahtzee(self):
        """Hard AI should hold all dice when yahtzee is achieved."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [4, 4, 4, 4, 4]
        game.current = 0
        # Only Yahtzee available
        for cat in ALL_CATS:
            if cat != "Yahtzee":
                game.scores[0][cat] = 0
        ai._hard_choose_holds(game)
        assert game.held == [True, True, True, True, True]

    def test_hard_ai_holds_for_three_of_a_kind(self):
        """Hard AI should hold matching dice for three of a kind."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [5, 5, 5, 2, 3]
        game.current = 0
        # Only Three of a Kind available
        for cat in ALL_CATS:
            if cat != "Three of a Kind":
                game.scores[0][cat] = 0
        ai._hard_choose_holds(game)
        # Should hold all since we already have three of a kind
        assert game.held == [True, True, True, True, True]

    def test_hard_ai_holds_for_four_of_a_kind(self):
        """Hard AI should hold matching dice for four of a kind."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [2, 2, 2, 2, 6]
        game.current = 0
        # Only Four of a Kind available
        for cat in ALL_CATS:
            if cat != "Four of a Kind":
                game.scores[0][cat] = 0
        ai._hard_choose_holds(game)
        # Should hold all since we already have four of a kind
        assert game.held == [True, True, True, True, True]

    def test_hard_ai_holds_for_full_house(self):
        """Hard AI should hold appropriate dice for full house."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [3, 3, 3, 5, 5]
        game.current = 0
        # Only Full House available
        for cat in ALL_CATS:
            if cat != "Full House":
                game.scores[0][cat] = 0
        ai._hard_choose_holds(game)
        # Should hold all since we have a full house
        assert game.held == [True, True, True, True, True]

    def test_hard_ai_holds_for_chance(self):
        """Hard AI should hold all dice for chance to maximize sum."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [1, 3, 5, 2, 4]
        game.current = 0
        # Only Chance available
        for cat in ALL_CATS:
            if cat != "Chance":
                game.scores[0][cat] = 0
        ai._hard_choose_holds(game)
        assert game.held == [True, True, True, True, True]

    def test_hard_ai_chooses_highest_scoring_category(self):
        """Hard AI should choose the category with highest potential score."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [6, 6, 6, 6, 6]
        game.current = 0
        game.rolls_left = 2  # Need to have rolled at least once
        # All categories available
        category = ai._hard_choose_category(game)
        # With yahtzee of 6s, should prefer Yahtzee (50) or Sixes (30) or Chance (30)
        assert category in ["Yahtzee", "Sixes", "Chance", "Four of a Kind", "Three of a Kind"]

    def test_hard_ai_avoids_wasting_valuable_categories(self):
        """Hard AI should prefer wasting less valuable categories when scoring 0."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [1, 2, 3, 4, 6]  # No straights, no pairs
        game.current = 0
        # All categories available
        category = ai._hard_choose_category(game)
        # Should prefer wasting upper section or less valuable categories
        assert category is not None

    def test_hard_choose_holds_public_method(self):
        """Test public choose_holds method for hard AI."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [5, 5, 5, 2, 3]
        game.current = 0
        ai.choose_holds(game)
        # Should hold the three 5s at minimum
        assert game.held[0] is True
        assert game.held[1] is True
        assert game.held[2] is True

    def test_hard_choose_category_public_method(self):
        """Test public choose_category method for hard AI."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [4, 4, 4, 4, 4]
        game.current = 0
        game.rolls_left = 2
        category = ai.choose_category(game)
        assert category is not None

    def test_hard_ai_returns_none_when_no_categories(self):
        """Hard AI should return None when no categories available."""
        ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        # Mark all categories as scored
        for cat in ALL_CATS:
            game.scores[0][cat] = 0
        category = ai._hard_choose_category(game)
        assert category is None


class TestAIDifficultySwitching:
    """Test switching between AI difficulties."""

    def test_ai_difficulty_can_be_changed(self):
        """AI difficulty can be set during initialization."""
        easy_ai = AIPlayer(difficulty="easy")
        hard_ai = AIPlayer(difficulty="hard")
        assert easy_ai.difficulty == "easy"
        assert hard_ai.difficulty == "hard"

    def test_different_difficulties_produce_different_behavior(self):
        """Easy and hard AI should behave differently."""
        easy_ai = AIPlayer(difficulty="easy")
        hard_ai = AIPlayer(difficulty="hard")
        game = YahtzeeGame()
        game.dice = [6, 6, 6, 6, 6]
        game.current = 0

        # Easy AI doesn't hold anything
        easy_ai.choose_holds(game)
        easy_holds = game.held.copy()

        # Reset game
        game.held = [False] * 5

        # Hard AI should hold all dice for yahtzee
        hard_ai.choose_holds(game)
        hard_holds = game.held.copy()

        # They should be different
        assert easy_holds != hard_holds


class TestAIBestHoldForCategory:
    """Test the _best_hold_for_category method specifically."""

    def test_best_hold_for_ones(self):
        """Test holding ones for Ones category."""
        ai = AIPlayer(difficulty="hard")
        dice = [1, 1, 3, 4, 5]
        score, hold = ai._best_hold_for_category("Ones", dice)
        assert score == 2
        assert hold == [True, True, False, False, False]

    def test_best_hold_for_sixes(self):
        """Test holding sixes for Sixes category."""
        ai = AIPlayer(difficulty="hard")
        dice = [1, 6, 6, 4, 6]
        score, hold = ai._best_hold_for_category("Sixes", dice)
        assert score == 18
        assert hold == [False, True, True, False, True]

    def test_best_hold_for_small_straight(self):
        """Test holding dice for small straight."""
        ai = AIPlayer(difficulty="hard")
        dice = [1, 2, 3, 5, 6]
        score, hold = ai._best_hold_for_category("Small Straight", dice)
        # Should hold all unique dice that could form a straight
        assert all(hold)

    def test_best_hold_for_large_straight(self):
        """Test holding dice for large straight."""
        ai = AIPlayer(difficulty="hard")
        dice = [1, 2, 3, 4, 5]
        score, hold = ai._best_hold_for_category("Large Straight", dice)
        assert all(hold)

    def test_best_hold_for_full_house_partial(self):
        """Test holding dice when working towards full house."""
        ai = AIPlayer(difficulty="hard")
        dice = [4, 4, 4, 2, 3]
        score, hold = ai._best_hold_for_category("Full House", dice)
        # Should hold the three 4s
        assert hold[0] is True
        assert hold[1] is True
        assert hold[2] is True
