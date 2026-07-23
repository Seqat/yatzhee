"""Main Tkinter application window with sound effects and multi-language support."""

import tkinter as tk
from tkinter import messagebox

from ..ai import AIPlayer
from ..constants import (
    ALL_CATS,
    DICE_COUNT,
    DOT_POSITIONS,
    LOWER_CATS,
    MAX_ROLLS,
    TOTAL_ROUNDS,
    UPPER_BONUS_THRESHOLD,
    UPPER_CATS,
)
from ..game import YahtzeeGame
from ..i18n import t
from ..settings import GameSettings
from ..sound import SoundManager
from ..theme import (
    ACCENT,
    BG,
    CARD,
    DOT_CLR,
    FREE_DIE,
    GOLD,
    HELD_DIE,
    HOVER,
    MUTED,
    P1_CLR,
    P2_CLR,
    PANEL,
    TEXT,
)
from .tooltip import Tooltip
from .widgets import rounded_rect


class YahtzeeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = GameSettings()
        self.sound = SoundManager(enabled=self.settings.get("sound_enabled", True))

        self.title(t("app_title", lang=self.lang))
        self.resizable(False, False)
        self.configure(bg=BG)
        self.game = YahtzeeGame()
        self.ai = None  # set if playing vs AI
        self.ai_turn = False  # True while AI is animating
        self._show_menu()

    @property
    def lang(self) -> str:
        return self.settings.get("language", "tr")

    def _create_badge_button(self, parent, text, command):
        """Create a custom high-contrast badge button compatible with all OSs."""
        btn = tk.Label(
            parent,
            text=text,
            bg="#21262d",
            fg="#58a6ff",
            font=("Courier New", 9, "bold"),
            padx=10,
            pady=4,
            cursor="hand2",
            relief="flat",
        )
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.config(bg="#30363d", fg="#79c0ff"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#21262d", fg="#58a6ff"))
        return btn

    def _toggle_sound(self):
        new_val = not self.sound.enabled
        self.sound.enabled = new_val
        self.settings.set("sound_enabled", new_val)
        if hasattr(self, "sound_btn"):
            lbl = t("sound_on", lang=self.lang) if new_val else t("sound_off", lang=self.lang)
            self.sound_btn.config(text=f"🔊 {lbl}")

    def _toggle_language(self):
        cur_lang = self.lang
        new_lang = "en" if cur_lang == "tr" else "tr"
        self.settings.set("language", new_lang)
        self.title(t("app_title", lang=new_lang))
        # Refresh current screen
        if hasattr(self, "roll_btn") and self.roll_btn.winfo_exists():
            self._build_ui()
            self._refresh()
        else:
            self._show_menu()

    # ── Mode Selection Screen ─────────────────────────────────────────────────
    def _show_menu(self):
        # Destroy game frames if they exist
        for w in self.winfo_children():
            w.destroy()

        self.game.reset()
        self.ai = None
        self.ai_turn = False

        # Top bar controls (Language & Sound)
        top_bar = tk.Frame(self, bg=BG, padx=10, pady=10)
        top_bar.pack(fill="x")

        lang_btn = self._create_badge_button(
            top_bar, f"🌐 {self.lang.upper()}", self._toggle_language
        )
        lang_btn.pack(side="left")

        sound_label = (
            t("sound_on", lang=self.lang) if self.sound.enabled else t("sound_off", lang=self.lang)
        )
        self.sound_btn = self._create_badge_button(top_bar, f"🔊 {sound_label}", self._toggle_sound)
        self.sound_btn.pack(side="right")

        menu = tk.Frame(self, bg=BG, padx=50, pady=30)
        menu.pack(expand=True)

        tk.Label(menu, text="🎲", bg=BG, fg=TEXT, font=("Courier New", 48)).pack(pady=(0, 4))
        tk.Label(menu, text="YAHTZEE", bg=BG, fg=ACCENT, font=("Courier New", 32, "bold")).pack()
        tk.Label(
            menu,
            text=t("game_mode", lang=self.lang),
            bg=BG,
            fg=MUTED,
            font=("Courier New", 11),
        ).pack(pady=(4, 28))

        btn_common = dict(
            font=("Courier New", 13, "bold"),
            fg="#1a1a2e",
            relief="flat",
            padx=30,
            pady=14,
            cursor="hand2",
            bd=0,
            width=22,
            activeforeground="#1a1a2e",
        )

        b1 = tk.Button(
            menu,
            text=f"👥  {t('mode_2p', lang=self.lang)}",
            command=lambda: self._start_game("local"),
            highlightbackground="#58a6ff",
            bg="#58a6ff",
            activebackground="#3a8ae0",
            **btn_common,
        )
        b1.pack(pady=5)

        b2 = tk.Button(
            menu,
            text=f"🤖  {t('mode_ai_easy', lang=self.lang)}",
            command=lambda: self._start_game("ai_easy"),
            highlightbackground="#3fb950",
            bg="#3fb950",
            activebackground="#2ea043",
            **btn_common,
        )
        b2.pack(pady=5)

        b3 = tk.Button(
            menu,
            text=f"🧠  {t('mode_ai_hard', lang=self.lang)}",
            command=lambda: self._start_game("ai_hard"),
            highlightbackground="#f78166",
            bg="#f78166",
            activebackground="#d05a46",
            **btn_common,
        )
        b3.pack(pady=5)

    def _start_game(self, mode):
        self.game.reset()
        if mode == "local":
            self.game.player_names = [
                self.settings.get("player_1_name", "Player 1"),
                self.settings.get("player_2_name", "Player 2"),
            ]
            self.ai = None
        elif mode == "ai_easy":
            self.game.player_names = [
                self.settings.get("player_1_name", "Player 1"),
                t("ai_name_easy", lang=self.lang),
            ]
            self.ai = AIPlayer("easy")
        elif mode == "ai_hard":
            self.game.player_names = [
                self.settings.get("player_1_name", "Player 1"),
                t("ai_name_hard", lang=self.lang),
            ]
            self.ai = AIPlayer("hard")

        # Destroy menu and build game UI
        for w in self.winfo_children():
            w.destroy()
        self._build_ui()
        self._refresh()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Destroy current children if rebuilding
        for w in self.winfo_children():
            w.destroy()

        left = tk.Frame(self, bg=BG, padx=20, pady=15)
        right = tk.Frame(self, bg=PANEL, padx=18, pady=18)
        left.grid(row=0, column=0, sticky="nsew")
        right.grid(row=0, column=1, sticky="nsew")

        # Top Bar in Left Pane (Language & Sound)
        top_bar = tk.Frame(left, bg=BG)
        top_bar.pack(fill="x", pady=(0, 10))

        lang_btn = self._create_badge_button(
            top_bar, f"🌐 {self.lang.upper()}", self._toggle_language
        )
        lang_btn.pack(side="left")

        sound_label = (
            t("sound_on", lang=self.lang) if self.sound.enabled else t("sound_off", lang=self.lang)
        )
        self.sound_btn = self._create_badge_button(top_bar, f"🔊 {sound_label}", self._toggle_sound)
        self.sound_btn.pack(side="right")

        # Title
        tk.Label(left, text="🎲  YAHTZEE", bg=BG, fg=ACCENT, font=("Courier New", 24, "bold")).pack(
            pady=(0, 2)
        )

        # Turn indicator
        self.turn_lbl = tk.Label(left, bg=BG, fg=P1_CLR, font=("Courier New", 13, "bold"))
        self.turn_lbl.pack(pady=(0, 2))

        self.info_lbl = tk.Label(left, bg=BG, fg=MUTED, font=("Courier New", 11))
        self.info_lbl.pack()

        # Dice row
        dice_frame = tk.Frame(left, bg=BG)
        dice_frame.pack(pady=16)
        self.die_canvases = []
        for i in range(DICE_COUNT):
            wrap = tk.Frame(dice_frame, bg=BG)
            wrap.grid(row=0, column=i, padx=5)
            c = tk.Canvas(wrap, width=76, height=76, bg=BG, highlightthickness=0, cursor="hand2")
            c.pack()
            c.bind("<Button-1>", lambda e, idx=i: self._toggle_hold(idx))
            self.die_canvases.append(c)
            tk.Label(wrap, text="HOLD", bg=BG, fg=MUTED, font=("Courier New", 7)).pack()

        # Roll button
        self.roll_btn = tk.Button(
            left,
            text=f"🎲   {t('roll_dice', lang=self.lang)}",
            command=self._roll,
            bg=ACCENT,
            fg="#1a1a2e",
            font=("Courier New", 13, "bold"),
            relief="flat",
            padx=28,
            pady=10,
            cursor="hand2",
            activebackground="#d05a46",
            activeforeground="#1a1a2e",
            bd=0,
            highlightbackground=ACCENT,
        )
        self.roll_btn.pack(pady=6)

        # Hints box
        hint_outer = tk.Frame(left, bg=CARD, padx=1, pady=1)
        hint_outer.pack(fill="x", pady=(12, 0))
        tk.Label(
            hint_outer,
            text="  POTENTIAL SCORES",
            bg=CARD,
            fg=MUTED,
            font=("Courier New", 9),
            anchor="w",
        ).pack(fill="x")
        self.hint_box = tk.Text(
            hint_outer,
            bg=CARD,
            fg=TEXT,
            font=("Courier New", 9),
            height=7,
            relief="flat",
            state="disabled",
            padx=8,
            pady=4,
            insertbackground=TEXT,
        )
        self.hint_box.pack(fill="x")
        self.hint_box.tag_config("hi", foreground=GOLD)
        self.hint_box.tag_config("dim", foreground=MUTED)

        # New game
        tk.Button(
            left,
            text=f"↺  {t('new_game', lang=self.lang)}",
            command=self._show_menu,
            bg=CARD,
            fg="#1a1a2e",
            font=("Courier New", 10),
            relief="flat",
            padx=14,
            pady=5,
            cursor="hand2",
            activebackground=HOVER,
            activeforeground="#1a1a2e",
            bd=0,
            highlightbackground=CARD,
        ).pack(pady=(14, 0))

        # ── Scorecard ──────────────────────────────────────────────────────
        tk.Label(
            right, text="SCORECARD", bg=PANEL, fg=ACCENT, font=("Courier New", 13, "bold")
        ).pack(pady=(0, 6))

        # Column headers
        hdr = tk.Frame(right, bg=PANEL)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="", bg=PANEL, width=16, anchor="w").pack(side="left")
        p1_name = self.game.player_names[0]
        p2_name = self.game.player_names[1]
        tk.Label(
            hdr,
            text=p1_name,
            bg=PANEL,
            fg=P1_CLR,
            font=("Courier New", 9, "bold"),
            width=10,
            anchor="e",
        ).pack(side="left")
        tk.Label(
            hdr,
            text=p2_name,
            bg=PANEL,
            fg=P2_CLR,
            font=("Courier New", 9, "bold"),
            width=10,
            anchor="e",
        ).pack(side="left")

        self.score_rows = {}

        tk.Label(right, text="─ UPPER SECTION ─", bg=PANEL, fg=MUTED, font=("Courier New", 8)).pack(
            anchor="w"
        )
        for cat in UPPER_CATS:
            self._score_row(right, cat)

        tk.Label(right, text="─ LOWER SECTION ─", bg=PANEL, fg=MUTED, font=("Courier New", 8)).pack(
            anchor="w", pady=(8, 0)
        )
        for cat in LOWER_CATS:
            self._score_row(right, cat)

        tk.Frame(right, bg=ACCENT, height=2).pack(fill="x", pady=10)

        # Totals for both players
        totals = tk.Frame(right, bg=PANEL)
        totals.pack(fill="x")

        self.upper_sub_lbls = []
        self.bonus_lbls = []
        self.total_lbls = []

        for p in range(2):
            clr = P1_CLR if p == 0 else P2_CLR
            name = self.game.player_names[p]
            tk.Label(
                totals,
                text=f"── {name} ──",
                bg=PANEL,
                fg=clr,
                font=("Courier New", 9, "bold"),
                anchor="w",
            ).pack(fill="x", pady=(4 if p else 0, 0))
            ul = tk.Label(totals, bg=PANEL, fg=TEXT, anchor="w", font=("Courier New", 9))
            bl = tk.Label(totals, bg=PANEL, fg=GOLD, anchor="w", font=("Courier New", 9))
            tl = tk.Label(totals, bg=PANEL, fg=clr, anchor="w", font=("Courier New", 14, "bold"))
            ul.pack(fill="x")
            bl.pack(fill="x")
            tl.pack(fill="x", pady=(2, 0))
            self.upper_sub_lbls.append(ul)
            self.bonus_lbls.append(bl)
            self.total_lbls.append(tl)

    def _score_row(self, parent, cat):
        row = tk.Frame(parent, bg=PANEL, cursor="hand2")
        row.pack(fill="x", pady=1)
        cat_disp = t(f"cat_{cat}", lang=self.lang)
        nl = tk.Label(
            row, text=cat_disp, bg=PANEL, fg=TEXT, font=("Courier New", 9), width=16, anchor="w"
        )
        nl.pack(side="left")
        # P1 score
        v1 = tk.Label(
            row, text="—", bg=PANEL, fg=MUTED, font=("Courier New", 9, "bold"), width=10, anchor="e"
        )
        v1.pack(side="left")
        # P2 score
        v2 = tk.Label(
            row, text="—", bg=PANEL, fg=MUTED, font=("Courier New", 9, "bold"), width=10, anchor="e"
        )
        v2.pack(side="left")

        # Store a leave-timer ID on the row for delayed leave
        row._leave_id = None

        for w in (row, nl, v1, v2):
            w.bind("<Button-1>", lambda e, c=cat: self._pick(c))
            w.bind("<Enter>", lambda e, r=row: self._hover_enter(r))
            w.bind("<Leave>", lambda e, r=row: self._hover_leave(r))

        self.score_rows[cat] = (row, nl, v1, v2)

        # Attach tooltip dynamically using current language
        Tooltip(nl, lambda c=cat: t(f"desc_{c}", lang=self.lang))

    def _hover_enter(self, row):
        # Cancel any pending leave
        if row._leave_id:
            self.after_cancel(row._leave_id)
            row._leave_id = None
        self._set_hover(row, True)

    def _hover_leave(self, row):
        if row._leave_id:
            self.after_cancel(row._leave_id)
        row._leave_id = self.after(50, lambda: self._set_hover(row, False))

    @staticmethod
    def _set_hover(row, on):
        bg = HOVER if on else PANEL
        row.config(bg=bg)
        for w in row.winfo_children():
            w.config(bg=bg)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _roll(self):
        if self.ai_turn:
            return
        if self.game.rolls_left > 0 and not self.game.game_over:
            self.sound.play("roll")
            self.game.roll()
            self._refresh()

    def _toggle_hold(self, idx):
        if self.ai_turn:
            return
        if self.game.rolls_left == MAX_ROLLS:
            return
        self.sound.play("hold")
        self.game.held[idx] = not self.game.held[idx]
        self._draw_dice()

    def _pick(self, cat):
        if self.ai_turn:
            return
        g = self.game
        if g.game_over:
            return
        if g.rolls_left == MAX_ROLLS:
            messagebox.showinfo("Yahtzee", "Roll the dice first!", parent=self)
            return
        p = g.current
        if g.scores[p][cat] is not None:
            messagebox.showinfo("Yahtzee", "Category already scored!", parent=self)
            return
        self.sound.play("score")
        g.assign(cat)
        self._refresh()
        if g.game_over:
            self.sound.play("win")
            self._end_game()
        elif self.ai and g.current == 1:
            self._start_ai_turn()

    def _start_ai_turn(self):
        """Kick off animated AI turn."""
        self.ai_turn = True
        self._refresh()
        self._ai_roll(0)

    def _ai_roll(self, roll_num):
        """AI rolls dice with animation delays."""
        g = self.game
        if g.game_over:
            self.ai_turn = False
            return

        if roll_num < 3:
            # Before rolls 2 and 3, choose which dice to hold
            if roll_num > 0:
                self.ai.choose_holds(g)
            self.sound.play("roll")
            g.roll()
            self._refresh()

            if roll_num < 2:
                # Schedule next roll
                self.after(700, lambda: self._ai_roll(roll_num + 1))
            else:
                # After last roll, pick category
                self.after(700, self._ai_pick)

    def _ai_pick(self):
        """AI picks the best category."""
        g = self.game
        cat = self.ai.choose_category(g)
        if cat:
            self.sound.play("score")
            g.assign(cat)
        self.ai_turn = False
        self._refresh()
        if g.game_over:
            self.sound.play("win")
            self._end_game()

    # ── Rendering ─────────────────────────────────────────────────────────────
    def _refresh(self):
        g = self.game
        p = g.current
        clr = P1_CLR if p == 0 else P2_CLR

        # Turn indicator
        if g.game_over:
            self.turn_lbl.config(text=t("game_over", lang=self.lang), fg=GOLD)
        elif self.ai_turn:
            self.turn_lbl.config(text=f"🤖 {g.current_name}…", fg=P2_CLR)
        else:
            self.turn_lbl.config(
                text=f"▸ {t('current_turn', lang=self.lang, name=g.current_name)}", fg=clr
            )

        rolls_str = "●" * g.rolls_left + "○" * (MAX_ROLLS - g.rolls_left)
        rnd = min(g.rounds[p], TOTAL_ROUNDS)
        round_txt = t("round_counter", lang=self.lang, current=rnd, total=TOTAL_ROUNDS)
        rolls_txt = t("rolls_left", lang=self.lang, count=rolls_str)
        self.info_lbl.config(text=f"{round_txt}   {rolls_txt}")
        can_roll = g.rolls_left > 0 and not g.game_over and not self.ai_turn
        self.roll_btn.config(
            text=f"🎲   {t('roll_dice', lang=self.lang)}",
            state="normal" if can_roll else "disabled",
            bg=ACCENT if can_roll else CARD,
        )
        self._draw_dice()
        self._update_scorecard()
        self._update_hints()

    def _draw_dice(self):
        g = self.game
        for i, c in enumerate(self.die_canvases):
            c.delete("all")
            held = g.held[i]
            color = HELD_DIE if held else FREE_DIE
            # Glow for held dice
            if held:
                rounded_rect(c, 2, 2, 74, 74, r=12, fill="#b8860b", outline="")
            rounded_rect(c, 5, 5, 71, 71, r=10, fill=color, outline="")
            # Dots
            for dx, dy in DOT_POSITIONS[g.dice[i]]:
                px = 5 + dx * 66
                py = 5 + dy * 66
                r = 5
                c.create_oval(px - r, py - r, px + r, py + r, fill=DOT_CLR, outline="")

    def _update_scorecard(self):
        g = self.game
        for cat, (row, nl, v1, v2) in self.score_rows.items():
            for p_idx, vl in enumerate([v1, v2]):
                s = g.scores[p_idx][cat]
                if s is not None:
                    vl.config(text=str(s), fg=GOLD if s > 0 else MUTED)
                else:
                    vl.config(text="—", fg=MUTED)
            # Dim the category name if BOTH players have scored it
            if g.scores[0][cat] is not None and g.scores[1][cat] is not None:
                nl.config(fg=MUTED)
            else:
                nl.config(fg=TEXT)

        for p in range(2):
            us = g.upper_subtotal(p)
            bonus = g.bonus(p)
            remaining = max(0, UPPER_BONUS_THRESHOLD - us)
            sub_title = t("cat_Upper Subtotal", lang=self.lang)
            bonus_title = t("cat_Bonus (63+)", lang=self.lang)
            tot_title = t("cat_Total", lang=self.lang)

            self.upper_sub_lbls[p].config(text=f"  {sub_title} : {us} / {UPPER_BONUS_THRESHOLD}")
            self.bonus_lbls[p].config(
                text=(f"  {bonus_title} : ✓ +35" if bonus else f"  {bonus_title} : {remaining}")
            )
            self.total_lbls[p].config(text=f"  {tot_title} : {g.total(p)}")

    def _update_hints(self):
        g = self.game
        p = g.current
        self.hint_box.config(state="normal")
        self.hint_box.delete("1.0", "end")
        if g.rolls_left < MAX_ROLLS and not g.game_over:
            rows = []
            for cat in ALL_CATS:
                if g.scores[p][cat] is None:
                    cat_tr = t(f"cat_{cat}", lang=self.lang)
                    rows.append((g.potential(cat), cat_tr))
            rows.sort(reverse=True)
            for pts, cat_name in rows:
                tag = "hi" if pts > 0 else "dim"
                self.hint_box.insert("end", f"  {cat_name:<22} {pts:>3}\n", tag)
        self.hint_box.config(state="disabled")

    def _end_game(self):
        g = self.game
        s0 = g.total(0)
        s1 = g.total(1)
        n0 = g.player_names[0]
        n1 = g.player_names[1]

        if s0 > s1:
            winner = t("winner", lang=self.lang, name=n0, score=s0)
        elif s1 > s0:
            winner = t("winner", lang=self.lang, name=n1, score=s1)
        else:
            winner = t("tie_game", lang=self.lang, score=s0)

        title = t("game_over", lang=self.lang)
        messagebox.showinfo(title, f"{n0}: {s0}  |  {n1}: {s1}\n\n{winner}", parent=self)
