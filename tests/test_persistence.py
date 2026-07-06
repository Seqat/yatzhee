"""Tests for persistence and settings."""

import tempfile
from pathlib import Path

import pytest

from src.yahtzee.persistence import HighScoreManager
from src.yahtzee.settings import GameSettings


class TestHighScoreManager:
    """Test high score persistence."""

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_load_empty_scores(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        scores = manager.load_scores()
        assert scores == []

    def test_add_and_load_score(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        manager.add_score("Alice", 250, "local")
        scores = manager.load_scores()
        assert len(scores) == 1
        assert scores[0]["player"] == "Alice"
        assert scores[0]["score"] == 250

    def test_scores_sorted_descending(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        manager.add_score("Alice", 250, "local")
        manager.add_score("Bob", 300, "local")
        manager.add_score("Charlie", 200, "local")

        scores = manager.load_scores()
        assert scores[0]["score"] == 300
        assert scores[1]["score"] == 250
        assert scores[2]["score"] == 200

    def test_is_high_score_empty_list(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        assert manager.is_high_score(100, min_rank=10)

    def test_is_high_score_partial_list(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        manager.add_score("Alice", 250, "local")
        assert manager.is_high_score(200, min_rank=10)

    def test_is_high_score_full_list(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        # Add 10 scores
        for i in range(10):
            manager.add_score(f"Player{i}", 100 + i * 10, "local")

        # Score above the 10th should be high
        assert manager.is_high_score(200, min_rank=10)
        # Score below the 10th should not be high
        assert not manager.is_high_score(90, min_rank=10)

    def test_limit_scores_to_50(self, temp_dir):
        manager = HighScoreManager(temp_dir)
        # Add 60 scores
        for i in range(60):
            manager.add_score(f"Player{i}", 1000 - i, "local")

        scores = manager.load_scores(limit=100)
        assert len(scores) <= 50


class TestGameSettings:
    """Test settings persistence."""

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_default_settings(self, temp_dir):
        settings = GameSettings(temp_dir)
        assert settings.get("theme") == "dark"
        assert settings.get("sound_enabled") is False
        assert settings.get("animations_enabled") is True

    def test_set_and_get(self, temp_dir):
        settings = GameSettings(temp_dir)
        settings.set("theme", "light")
        assert settings.get("theme") == "light"

    def test_settings_persist_to_disk(self, temp_dir):
        settings = GameSettings(temp_dir)
        settings.set("theme", "light")
        settings.set("sound_enabled", True)

        # Create new instance from same directory
        settings2 = GameSettings(temp_dir)
        assert settings2.get("theme") == "light"
        assert settings2.get("sound_enabled") is True

    def test_get_with_default(self, temp_dir):
        settings = GameSettings(temp_dir)
        value = settings.get("nonexistent", "default_value")
        assert value == "default_value"

    def test_reset_to_defaults(self, temp_dir):
        settings = GameSettings(temp_dir)
        settings.set("theme", "light")
        settings.set("sound_enabled", True)

        settings.reset_to_defaults()
        assert settings.get("theme") == "dark"
        assert settings.get("sound_enabled") is False

    def test_invalid_settings_file(self, temp_dir):
        # Write invalid JSON
        settings_file = temp_dir / "settings.json"
        with open(settings_file, "w") as f:
            f.write("invalid json {")

        # Should load defaults on error
        settings = GameSettings(temp_dir)
        assert settings.get("theme") == "dark"
