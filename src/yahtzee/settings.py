"""Game settings and preferences."""

import json
from pathlib import Path
from typing import Any


class GameSettings:
    """Manages game preferences and settings."""

    DEFAULT_SETTINGS = {
        "theme": "dark",  # "dark" or "light"
        "sound_enabled": False,
        "animations_enabled": True,
        "ai_difficulty": "easy",  # "easy" or "hard"
        "player_1_name": "Player 1",
        "player_2_name": "Player 2",
    }

    def __init__(self, data_dir: Path | None = None):
        """Initialize settings manager.

        Args:
            data_dir: Directory to store settings. Defaults to ~/.yahtzee
        """
        if data_dir is None:
            data_dir = Path.home() / ".yahtzee"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.settings_file = self.data_dir / "settings.json"
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        """Load settings from disk."""
        if not self.settings_file.exists():
            return

        try:
            with open(self.settings_file, "r") as f:
                loaded = json.load(f)
            # Merge with defaults to handle new keys
            self.settings = {**self.DEFAULT_SETTINGS, **loaded}
        except (json.JSONDecodeError, IOError):
            pass  # Keep defaults on error

    def save(self):
        """Save settings to disk."""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't write

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set a setting value and save to disk.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        self.save()

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
