"""Tests for the sound manager module."""

from src.yahtzee.sound import SoundManager, _generate_wav


def test_wav_generation():
    """Test generating WAV bytes from floating point samples."""
    samples = [0.0, 0.5, -0.5, 1.0, -1.0]
    wav_bytes = _generate_wav(samples, sample_rate=22050)
    assert isinstance(wav_bytes, bytes)
    assert len(wav_bytes) > 44  # Standard WAV header is 44 bytes


def test_sound_manager_initialization():
    """Test sound manager initializes pre-rendered sound effects."""
    sound_mgr = SoundManager(enabled=True)
    assert "roll" in sound_mgr._sound_files
    assert "hold" in sound_mgr._sound_files
    assert "score" in sound_mgr._sound_files
    assert "win" in sound_mgr._sound_files
    sound_mgr.cleanup()


def test_sound_manager_play_disabled():
    """Test playing sound when disabled does nothing."""
    sound_mgr = SoundManager(enabled=False)
    # Should complete without error or side-effect
    sound_mgr.play("roll")


def test_sound_manager_play_invalid():
    """Test playing invalid sound name does not raise error."""
    sound_mgr = SoundManager(enabled=True)
    sound_mgr.play("non_existent_sound")


def test_sound_manager_play_enabled():
    """Test playing valid sound when enabled executes safely."""
    sound_mgr = SoundManager(enabled=True)
    sound_mgr.play("roll")
