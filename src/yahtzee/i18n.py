"""Internationalization (i18n) module for Yahtzee supporting English and Turkish."""

from __future__ import annotations

from typing import Any

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        # General UI
        "app_title": "Yahtzee",
        "new_game": "New Game",
        "roll_dice": "Roll Dice",
        "rolls_left": "Rolls Left: {count}",
        "game_over": "Game Over!",
        "winner": "Winner: {name} ({score} pts)!",
        "tie_game": "It's a Tie ({score} pts)!",
        "round_counter": "Round {current}/{total}",
        "current_turn": "{name}'s Turn",
        "hold_instruction": "Click dice to hold / release",
        # Categories
        "cat_Ones": "Ones",
        "cat_Twos": "Twos",
        "cat_Threes": "Threes",
        "cat_Fours": "Fours",
        "cat_Fives": "Fives",
        "cat_Sixes": "Sixes",
        "cat_Three of a Kind": "Three of a Kind",
        "cat_Four of a Kind": "Four of a Kind",
        "cat_Full House": "Full House",
        "cat_Small Straight": "Small Straight",
        "cat_Large Straight": "Large Straight",
        "cat_Yahtzee": "Yahtzee",
        "cat_Chance": "Chance",
        "cat_Upper Subtotal": "Upper Subtotal",
        "cat_Bonus (63+)": "Bonus (63+)",
        "cat_Total": "Total Score",
        # Tooltips
        "desc_Ones": "Count and add only 1s",
        "desc_Twos": "Count and add only 2s",
        "desc_Threes": "Count and add only 3s",
        "desc_Fours": "Count and add only 4s",
        "desc_Fives": "Count and add only 5s",
        "desc_Sixes": "Count and add only 6s",
        "desc_Three of a Kind": "At least 3 dice the same. Scores sum of all 5 dice.",
        "desc_Four of a Kind": "At least 4 dice the same. Scores sum of all 5 dice.",
        "desc_Full House": "Three of one number and two of another. Scores 25 points.",
        "desc_Small Straight": "Sequence of 4 consecutive dice. Scores 30 points.",
        "desc_Large Straight": "Sequence of 5 consecutive dice. Scores 40 points.",
        "desc_Yahtzee": "All 5 dice the same. Scores 50 points.",
        "desc_Chance": "Any combination of dice. Scores sum of all 5 dice.",
        "desc_Bonus": "Score 35 bonus points if upper section subtotal is 63 or higher.",
        # Settings & Dialogs
        "settings": "Settings",
        "sound": "Sound Effects",
        "sound_on": "Sound: ON",
        "sound_off": "Sound: OFF",
        "language": "Language / Dil",
        "game_mode": "Game Mode",
        "mode_2p": "2 Players (Local)",
        "mode_ai_easy": "vs AI (Easy)",
        "mode_ai_hard": "vs AI (Hard)",
        "high_scores": "High Scores",
        "no_high_scores": "No high scores yet!",
        "score_unit": "pts",
        "date": "Date",
        "player": "Player",
        "score": "Score",
        "close": "Close",
        "reset": "Reset",
        "ai_name_easy": "AI (Easy)",
        "ai_name_hard": "AI (Hard)",
    },
    "tr": {
        # General UI
        "app_title": "Yahtzee",
        "new_game": "Yeni Oyun",
        "roll_dice": "Zar At",
        "rolls_left": "Kalan Zar Hakkı: {count}",
        "game_over": "Oyun Bitti!",
        "winner": "Kazanan: {name} ({score} Puan)!",
        "tie_game": "Berabere ({score} Puan)!",
        "round_counter": "Tur {current}/{total}",
        "current_turn": "Sıra: {name}",
        "hold_instruction": "Tutmak / bırakmak için zara tıklayın",
        # Categories
        "cat_Ones": "Birliler",
        "cat_Twos": "İkililer",
        "cat_Threes": "Üçlüler",
        "cat_Fours": "Dörtlüler",
        "cat_Fives": "Beşliler",
        "cat_Sixes": "Altılılar",
        "cat_Three of a Kind": "3'lü Takım",
        "cat_Four of a Kind": "4'lü Takım",
        "cat_Full House": "Full House",
        "cat_Small Straight": "Küçük Kent",
        "cat_Large Straight": "Büyük Kent",
        "cat_Yahtzee": "Yahtzee",
        "cat_Chance": "Şans",
        "cat_Upper Subtotal": "Üst Bölüm Toplamı",
        "cat_Bonus (63+)": "Bonus (63+)",
        "cat_Total": "Toplam Skor",
        # Tooltips
        "desc_Ones": "Sadece 1 olan zarları toplayın",
        "desc_Twos": "Sadece 2 olan zarları toplayın",
        "desc_Threes": "Sadece 3 olan zarları toplayın",
        "desc_Fours": "Sadece 4 olan zarları toplayın",
        "desc_Fives": "Sadece 5 olan zarları toplayın",
        "desc_Sixes": "Sadece 6 olan zarları toplayın",
        "desc_Three of a Kind": "En az 3 aynı zar. Tüm zarların toplamı yazılır.",
        "desc_Four of a Kind": "En az 4 aynı zar. Tüm zarların toplamı yazılır.",
        "desc_Full House": "3 aynı + 2 aynı zar (Full). 25 puan kazandırır.",
        "desc_Small Straight": "4 ardışık zar (örn: 1-2-3-4). 30 puan kazandırır.",
        "desc_Large Straight": "5 ardışık zar (örn: 1-2-3-4-5). 40 puan kazandırır.",
        "desc_Yahtzee": "5 zarın hepsi aynı. 50 puan kazandırır.",
        "desc_Chance": "Herhangi bir kombinasyon. Tüm zarların toplamı yazılır.",
        "desc_Bonus": "Üst bölüm toplamı 63 veya üzeri olursa +35 ekstra bonus kazanılır.",
        # Settings & Dialogs
        "settings": "Ayarlar",
        "sound": "Ses Efektleri",
        "sound_on": "Ses: Açık",
        "sound_off": "Ses: Kapalı",
        "language": "Dil / Language",
        "game_mode": "Oyun Modu",
        "mode_2p": "2 Oyuncu (Yerel)",
        "mode_ai_easy": "Yapay Zekâ (Kolay)",
        "mode_ai_hard": "Yapay Zekâ (Zor)",
        "high_scores": "Yüksek Skorlar",
        "no_high_scores": "Henüz yüksek skor yok!",
        "score_unit": "Puan",
        "date": "Tarih",
        "player": "Oyuncu",
        "score": "Skor",
        "close": "Kapat",
        "reset": "Sıfırla",
        "ai_name_easy": "Yapay Zekâ (Kolay)",
        "ai_name_hard": "Yapay Zekâ (Zor)",
    },
}


def t(key: str, lang: str = "tr", **kwargs: Any) -> str:
    """Get localized text for a translation key.

    Args:
        key: Translation key string
        lang: Target language code ('en' or 'tr')
        **kwargs: Values for formatting template variables in text

    Returns:
        Translated and formatted string.
    """
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text
