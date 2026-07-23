"""Tests for internationalization (i18n) module."""

from src.yahtzee.i18n import TRANSLATIONS, t


def test_translation_keys_exist_in_both_languages():
    """Ensure all keys in English dictionary exist in Turkish dictionary."""
    en_keys = set(TRANSLATIONS["en"].keys())
    tr_keys = set(TRANSLATIONS["tr"].keys())
    assert en_keys == tr_keys, f"Missing keys in translations: {en_keys ^ tr_keys}"


def test_t_function_basic():
    """Test basic translation lookup for English and Turkish."""
    assert t("roll_dice", lang="en") == "Roll Dice"
    assert t("roll_dice", lang="tr") == "Zar At"


def test_t_function_formatting():
    """Test string formatting within translation helper."""
    en_str = t("rolls_left", lang="en", count=2)
    tr_str = t("rolls_left", lang="tr", count=2)
    assert en_str == "Rolls Left: 2"
    assert tr_str == "Kalan Zar Hakkı: 2"


def test_t_function_fallback():
    """Test fallback when unknown language or missing key is requested."""
    assert t("roll_dice", lang="unknown_lang") == "Roll Dice"
    assert t("unknown_key_xyz", lang="tr") == "unknown_key_xyz"
