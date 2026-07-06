"""Tests for the game state and turn flow."""

import pytest
from src.yahtzee.game import YahtzeeGame
from src.yahtzee.constants import MAX_ROLLS, TOTAL_ROUNDS, UPPER_BONUS_THRESHOLD, UPPER_BONUS


class TestGameInitialization:
    """Test game initialization and reset."""

    def test_initial_state(self):
        game = YahtzeeGame()
        assert game.current == 0
        assert game.game_over is False
        assert game.rolls_left == MAX_ROLLS
        assert game.rounds == [1, 1]
        assert game.dice == [1, 1, 1, 1, 1]
        assert game.held == [False, False, False, False, False]

    def test_reset_clears_scores(self):
        game = YahtzeeGame()
        game.reset()
        for p in range(2):
            for cat, score in game.scores[p].items():
                assert score is None


class TestRolling:
    """Test dice rolling mechanics."""

    def test_roll_reduces_rolls_left(self):
        game = YahtzeeGame()
        assert game.rolls_left == MAX_ROLLS
        game.roll()
        assert game.rolls_left == MAX_ROLLS - 1
        game.roll()
        assert game.rolls_left == MAX_ROLLS - 2

    def test_roll_max_three_times(self):
        game = YahtzeeGame()
        for _ in range(MAX_ROLLS):
            game.roll()
        assert game.rolls_left == 0
        # Fourth roll should not decrease further
        game.roll()
        assert game.rolls_left == 0

    def test_held_dice_not_rerolled(self):
        game = YahtzeeGame()
        game.dice = [1, 2, 3, 4, 5]
        game.held = [True, False, False, False, False]  # Hold first die
        original_first = game.dice[0]
        game.roll()
        assert game.dice[0] == original_first  # First die should not change

    def test_roll_after_game_over_does_nothing(self):
        game = YahtzeeGame()
        game.game_over = True
        game.roll()
        assert game.rolls_left == MAX_ROLLS  # Should not decrease


class TestCategoryAssignment:
    """Test assigning scores to categories."""

    def test_assign_category_success(self):
        game = YahtzeeGame()
        game.roll()  # First roll
        # Now rolls_left is 2, can assign
        original_potential = game.potential("Chance")
        assert original_potential > 0  # Should have some potential
        success, reason = game.assign("Chance")
        assert success
        assert game.scores[0]["Chance"] == original_potential

    def test_cannot_assign_without_rolling(self):
        game = YahtzeeGame()
        # rolls_left is still MAX_ROLLS, cannot assign
        success, reason = game.assign("Ones")
        assert not success

    def test_cannot_assign_same_category_twice(self):
        game = YahtzeeGame()
        game.roll()
        success, reason = game.assign("Ones")
        assert success
        # Ones is now taken for player 0
        assert game.scores[0]["Ones"] is not None
        # Switch back to player 0 for next turn to try assigning again
        game.current = 0
        success, reason = game.assign("Ones")
        assert not success  # Should fail

    def test_assign_switches_player(self):
        game = YahtzeeGame()
        assert game.current == 0
        game.roll()
        success, reason = game.assign("Ones")
        assert success
        assert game.current == 1

    def test_assign_resets_dice_state(self):
        game = YahtzeeGame()
        game.roll()
        game.held = [True, False, True, False, False]
        success, reason = game.assign("Ones")
        assert success
        # After assignment, dice state should reset for next turn
        assert game.held == [False, False, False, False, False]
        assert game.rolls_left == MAX_ROLLS


class TestTurnFlow:
    """Test turn alternation and game progression."""

    def test_players_alternate(self):
        game = YahtzeeGame()
        # Track which player is current after each assignment
        assignments = []
        categories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
        for turn in range(6):
            assignments.append(game.current)
            game.roll()
            success, reason = game.assign(categories[turn])
            assert success
        
        # Players should alternate: 0, 1, 0, 1, 0, 1, ...
        assert assignments == [0, 1, 0, 1, 0, 1]

    def test_round_counter_increments(self):
        game = YahtzeeGame()
        assert game.rounds[0] == 1
        game.roll()
        game.assign("Ones")
        assert game.rounds[0] == 2  # Player 0 should be on round 2
        assert game.rounds[1] == 1  # Player 1 still on round 1

    def test_game_over_when_both_players_complete(self):
        game = YahtzeeGame()
        game.game_over = False
        game.rounds = [TOTAL_ROUNDS + 1, TOTAL_ROUNDS]
        # Not game over yet, only player 0 is done
        game.current = 1
        game.roll()
        game.assign("Chance")
        # Now both are done, should be game over
        assert game.game_over is True


class TestBonusLogic:
    """Test upper section bonus calculation."""

    def test_no_bonus_below_threshold(self):
        game = YahtzeeGame()
        # Manually set scores below threshold
        game.scores[0] = {
            "Ones": 5, "Twos": 4, "Threes": 6, "Fours": 0, "Fives": 0, "Sixes": 0,
            "Three of a Kind": None, "Four of a Kind": None, "Full House": None,
            "Small Straight": None, "Large Straight": None, "Yahtzee": None, "Chance": None,
        }
        upper_sub = game.upper_subtotal(0)
        assert upper_sub < UPPER_BONUS_THRESHOLD
        assert game.bonus(0) == 0

    def test_bonus_at_threshold(self):
        game = YahtzeeGame()
        # Set scores to exactly the threshold
        game.scores[0] = {
            "Ones": 5, "Twos": 10, "Threes": 15, "Fours": 16, "Fives": 10, "Sixes": 7,
            "Three of a Kind": None, "Four of a Kind": None, "Full House": None,
            "Small Straight": None, "Large Straight": None, "Yahtzee": None, "Chance": None,
        }
        upper_sub = game.upper_subtotal(0)
        assert upper_sub >= UPPER_BONUS_THRESHOLD
        assert game.bonus(0) == UPPER_BONUS

    def test_total_includes_bonus(self):
        game = YahtzeeGame()
        game.scores[0] = {
            "Ones": 5, "Twos": 10, "Threes": 15, "Fours": 16, "Fives": 10, "Sixes": 7,
            "Three of a Kind": None, "Four of a Kind": None, "Full House": None,
            "Small Straight": None, "Large Straight": None, "Yahtzee": None, "Chance": None,
        }
        upper_sub = game.upper_subtotal(0)
        total = game.total(0)
        assert total == upper_sub + UPPER_BONUS

    def test_lower_section_scores_count_in_total(self):
        game = YahtzeeGame()
        game.scores[0] = {
            "Ones": 5, "Twos": 10, "Threes": 15, "Fours": 16, "Fives": 10, "Sixes": 7,
            "Three of a Kind": 25, "Four of a Kind": None, "Full House": None,
            "Small Straight": None, "Large Straight": None, "Yahtzee": None, "Chance": None,
        }
        upper_sub = game.upper_subtotal(0)
        total = game.total(0)
        # Total should be upper + bonus + three of a kind
        assert total == upper_sub + UPPER_BONUS + 25


class TestPotentialScores:
    """Test the potential method for calculating scores without assigning."""

    def test_potential_without_assignment(self):
        game = YahtzeeGame()
        game.dice = [1, 1, 1, 4, 5]
        game.held = [True, True, True, True, True]  # Hold all to prevent re-roll
        game.roll()  # Necessary to enable potential calculation
        potential = game.potential("Ones")
        assert potential == 3  # Three ones
        assert game.scores[0]["Ones"] is None  # Not actually assigned

    def test_potential_for_all_categories(self):
        game = YahtzeeGame()
        game.dice = [1, 2, 3, 4, 5]
        game.held = [True, True, True, True, True]  # Hold all to prevent re-roll
        game.roll()
        # Should calculate potential for any category
        assert game.potential("Ones") == 1
        assert game.potential("Twos") == 2
        assert game.potential("Chance") == 15
        assert game.potential("Small Straight") == 30


class TestPlayerNames:
    """Test player name handling."""

    def test_current_player_name(self):
        game = YahtzeeGame()
        assert game.current_name == "Player 1"
        game.current = 1
        assert game.current_name == "Player 2"

    def test_custom_player_names(self):
        game = YahtzeeGame()
        game.player_names = ["Alice", "Bob"]
        assert game.current_name == "Alice"
