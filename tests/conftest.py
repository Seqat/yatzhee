"""Pytest configuration for Yahtzee tests."""

import sys
from pathlib import Path

# Add src to the path so imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
