"""Tests for the Tkinter GUI application, widgets, tooltips, theme, and main entrypoint."""

import tkinter as tk
from unittest.mock import MagicMock, patch
import pytest

from yahtzee import main
from yahtzee.ui.app import YahtzeeApp
from yahtzee.ui.tooltip import Tooltip
from yahtzee.ui.widgets import rounded_rect
from yahtzee import theme


@pytest.fixture
def app():
    """Fixture providing a hidden YahtzeeApp instance."""
    application = YahtzeeApp()
    application.withdraw()  # Prevent window popping up during tests
    yield application
    try:
        application.destroy()
    except tk.TclError:
        pass


def test_theme_constants():
    """Verify theme palette constants are string colors."""
    assert isinstance(theme.BG, str)
    assert isinstance(theme.PANEL, str)
    assert isinstance(theme.CARD, str)
    assert isinstance(theme.ACCENT, str)
    assert isinstance(theme.GOLD, str)
    assert isinstance(theme.TEXT, str)
    assert isinstance(theme.MUTED, str)
    assert isinstance(theme.HELD_DIE, str)
    assert isinstance(theme.FREE_DIE, str)
    assert isinstance(theme.DOT_CLR, str)
    assert isinstance(theme.HOVER, str)
    assert isinstance(theme.P1_CLR, str)
    assert isinstance(theme.P2_CLR, str)


def test_widgets_rounded_rect(app):
    """Test canvas rounded_rect creation."""
    canvas = tk.Canvas(app, width=100, height=100)
    poly = rounded_rect(canvas, 10, 10, 90, 90, r=10, fill="red")
    assert poly is not None
    assert len(canvas.find_all()) == 1


def test_tooltip_behavior(app):
    """Test Tooltip show and hide lifecycle."""
    lbl = tk.Label(app, text="Hover me")
    lbl.pack()
    
    # Tooltip with static text
    tt_static = Tooltip(lbl, "Static Tooltip")
    tt_static._show()
    assert tt_static.tip_window is not None
    tt_static._hide()
    assert tt_static.tip_window is None

    # Tooltip with callable text
    tt_dynamic = Tooltip(lbl, lambda: "Dynamic Tooltip")
    tt_dynamic._schedule_show()
    tt_dynamic._show()
    assert tt_dynamic.tip_window is not None
    tt_dynamic._schedule_hide()
    tt_dynamic._hide()
    assert tt_dynamic.tip_window is None


def test_app_initialization_and_settings(app):
    """Test app initialization and language/sound toggling."""
    assert app.game is not None
    assert app.lang in ("tr", "en")
    
    initial_sound = app.sound.enabled
    app._toggle_sound()
    assert app.sound.enabled == (not initial_sound)

    cur_lang = app.lang
    app._toggle_language()
    assert app.lang != cur_lang


def test_app_game_modes(app):
    """Test starting game modes (local, ai_easy, ai_hard)."""
    app._start_game("local")
    assert app.ai is None
    assert app.game.player_names[0] == "Player 1"

    app._start_game("ai_easy")
    assert app.ai is not None
    assert app.ai.difficulty == "easy"

    app._start_game("ai_hard")
    assert app.ai is not None
    assert app.ai.difficulty == "hard"


def test_app_roll_and_hold_dice(app):
    """Test rolling dice and toggling hold state in UI."""
    app._start_game("local")
    
    # Cannot hold dice before rolling
    app._toggle_hold(0)
    assert not app.game.held[0]

    # Roll dice
    app._roll()
    assert app.game.rolls_left == 2

    # Hold die 0
    app._toggle_hold(0)
    assert app.game.held[0]
    
    # Toggle hold die 0 back
    app._toggle_hold(0)
    assert not app.game.held[0]


@patch("tkinter.messagebox.showinfo")
def test_app_pick_category_validations(mock_showinfo, app):
    """Test category picking validations (before roll & already scored)."""
    app._start_game("local")

    # Pick category before rolling
    app._pick("Ones")
    mock_showinfo.assert_called_once()
    mock_showinfo.reset_mock()

    # Roll dice and pick category
    app._roll()
    app._pick("Ones")
    assert app.game.scores[0]["Ones"] is not None

    # Roll dice again for player 2 and try to pick already scored Ones for P1 turn later...
    # For now, turn switched to P2. P2 rolls and picks Ones (valid for P2).
    app._roll()
    app._pick("Ones")
    assert app.game.scores[1]["Ones"] is not None

    # Round 2 P1: Roll and try to pick Ones again (already scored for P1)
    app._roll()
    app._pick("Ones")
    mock_showinfo.assert_called_once()


def test_app_hover_handlers(app):
    """Test hover enter and leave handlers for scorecard rows."""
    app._start_game("local")
    cat = "Ones"
    row, nl, v1, v2 = app.score_rows[cat]

    app._hover_enter(row)
    assert row.cget("bg") == theme.HOVER

    app._hover_leave(row)
    app.update()  # Process pending after timer or idle tasks


def test_app_ai_turn_flow(app):
    """Test AI turn execution flow."""
    app._start_game("ai_easy")
    
    # Player 1 turn: roll and pick category
    app._roll()
    with patch.object(app, "after", lambda ms, func: func()):
        app._pick("Ones")

    # Verify AI completed its turn and back to P1 or game state updated
    assert app.game.current == 0 or app.game.game_over


@patch("tkinter.messagebox.showinfo")
def test_app_end_game(mock_showinfo, app):
    """Test end game popup logic."""
    app._start_game("local")
    app.game.scores[0]["Ones"] = 10
    app.game.scores[1]["Ones"] = 5
    app._end_game()
    mock_showinfo.assert_called_once()


def test_main_entrypoint():
    """Test main() entrypoint."""
    with patch("yahtzee.ui.app.YahtzeeApp") as mock_app_class:
        mock_instance = MagicMock()
        mock_app_class.return_value = mock_instance
        main()
        mock_app_class.assert_called_once()
        mock_instance.mainloop.assert_called_once()
