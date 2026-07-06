"""Tests for game validation and state queries."""

import pytest
from src.yahtzee.game import YahtzeeGame
from src.yahtzee.constants import MAX_ROLLS, UPPER_BONUS_THRESHOLD, UPPER_BONUS


class TestGameValidation:
    """Test validation methods and error reporting."""

    def test_can_roll_after_init(self):
        game = YahtzeeGame()
        assert game.can_roll()

    def test_cannot_roll_after_max_rolls(self):
        game = YahtzeeGame()
        for _ in range(MAX_ROLLS):
            game.roll()
        assert not game.can_roll()

    def test_cannot_roll_after_game_over(self):
        game = YahtzeeGame()
        game.game_over = True
        assert not game.can_roll()

    def test_can_assign_returns_tuple(self):
        game = YahtzeeGame()
        game.roll()
        success, reason = game.assign("Ones")
        assert isinstance(success, bool)
        assert isinstance(reason, str)

    def test_assign_invalid_category(self):
        game = YahtzeeGame()
        game.roll()
        success, reason = game.assign("NotACategory")
        assert not success
        assert "Invalid category" in reason

    def test_assign_without_rolling(self):
        game = YahtzeeGame()
        success, reason = game.assign("Ones")
        assert not success
        assert "Must roll" in reason

    def test_assign_already_scored(self):
        game = YahtzeeGame()
        game.roll()
        game.assign("Ones")
        # Now player 1's turn
        game.roll()
        game.assign("Ones")
        # Back to player 0, try to assign Ones again
        game.current = 0
        game.roll()
        success, reason = game.assign("Ones")
        assert not success
        assert "already scored" in reason

    def test_assign_after_game_over(self):
        game = YahtzeeGame()
        game.game_over = True
        game.roll()
        success, reason = game.assign("Ones")
        assert not success
        assert "Game is over" in reason


class TestGameStateQueries:
    """Test helper methods for game state."""

    def test_can_assign_simple_check(self):
        game = YahtzeeGame()
        game.roll()
        assert game.can_assign("Ones")
        success, _ = game.assign("Ones")
        assert success
        # Now it's player 1's turn
        game.roll()
        assert game.can_assign("Twos")

    def test_cannot_assign_after_already_scoring(self):
        game = YahtzeeGame()
        # Player 0 scores Ones
        game.roll()
        success, _ = game.assign("Ones")
        assert success
        # Player 1 tries to score Ones (should be able to)
        game.roll()
        assert game.can_assign("Ones")
        success, _ = game.assign("Ones")
        assert success
        # Player 0 tries to score Ones again (should fail)
        game.roll()
        assert not game.can_assign("Ones")

    def test_get_available_categories(self):
        game = YahtzeeGame()
        available = game.get_available_categories()
        assert len(available) == 13
        assert "Ones" in available
        
        game.roll()
        success, _ = game.assign("Ones")
        assert success
        # Now player 1's turn, should still have Ones available
        available = game.get_available_categories()
        assert "Ones" in available
        
        # Player 1 scores Ones
        game.roll()
        success, _ = game.assign("Ones")
        assert success
        # Back to player 0, Ones should not be available
        available = game.get_available_categories()
        assert "Ones" not in available

    def test_get_scores_summary(self):
        game = YahtzeeGame()
        summary = game.get_scores_summary()
        
        assert "player_names" in summary
        assert "scores" in summary
        assert "totals" in summary
        assert "upper_subtotals" in summary
        assert "bonuses" in summary
        assert len(summary["player_names"]) == 2
        assert len(summary["totals"]) == 2


class TestRollValidation:
    """Test improved roll method with return values."""

    def test_roll_returns_success(self):
        game = YahtzeeGame()
        result = game.roll()
        assert result is True

    def test_roll_returns_false_when_game_over(self):
        game = YahtzeeGame()
        game.game_over = True
        result = game.roll()
        assert result is False

    def test_roll_returns_false_after_max(self):
        game = YahtzeeGame()
        for _ in range(MAX_ROLLS):
            game.roll()
        result = game.roll()
        assert result is False
