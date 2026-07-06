"""High score persistence for Yahtzee."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


class HighScoreManager:
    """Manages high scores stored to disk."""

    def __init__(self, data_dir: Path | None = None):
        """Initialize the high score manager.

        Args:
            data_dir: Directory to store high score data. Defaults to ~/.yahtzee
        """
        if data_dir is None:
            data_dir = Path.home() / ".yahtzee"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.scores_file = self.data_dir / "high_scores.json"

    def load_scores(self, limit: int = 10) -> List[Dict]:
        """Load high scores from disk.

        Args:
            limit: Maximum number of scores to return

        Returns:
            List of score dictionaries sorted by score descending
        """
        if not self.scores_file.exists():
            return []

        try:
            with open(self.scores_file, "r") as f:
                scores = json.load(f)
            # Sort by score descending, then by timestamp
            scores.sort(key=lambda x: (-x["score"], -x.get("timestamp", 0)))
            return scores[:limit]
        except (json.JSONDecodeError, IOError):
            return []

    def add_score(self, player_name: str, score: int, game_type: str = "local"):
        """Add a new high score.

        Args:
            player_name: Name of the player
            score: Final score
            game_type: Type of game ("local", "ai_easy", "ai_hard")
        """
        import time

        scores = self.load_scores(limit=100)  # Keep more in memory to check if it's a high score

        new_entry = {
            "player": player_name,
            "score": score,
            "game_type": game_type,
            "timestamp": int(time.time()),
        }
        scores.append(new_entry)
        scores.sort(key=lambda x: (-x["score"], -x.get("timestamp", 0)))

        # Keep top 50
        scores = scores[:50]

        try:
            with open(self.scores_file, "w") as f:
                json.dump(scores, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't write

    def is_high_score(self, score: int, min_rank: int = 10) -> bool:
        """Check if a score would make the high score list.

        Args:
            score: The score to check
            min_rank: Maximum rank to consider a high score

        Returns:
            True if the score would be in the top min_rank
        """
        scores = self.load_scores(limit=min_rank)
        if len(scores) < min_rank:
            return True
        return score > scores[-1]["score"]
