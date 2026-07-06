"""Main Tkinter application window."""

import tkinter as tk
from tkinter import messagebox

from ..ai import AIPlayer
from ..constants import (
    ALL_CATS,
    CATEGORY_HINTS,
    DICE_COUNT,
    DOT_POSITIONS,
    LOWER_CATS,
    MAX_ROLLS,
    TOTAL_ROUNDS,
    UPPER_BONUS_THRESHOLD,
    UPPER_CATS,
)
from ..game import YahtzeeGame
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
        self.title("Yahtzee")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.game = YahtzeeGame()
        self.ai = None  # set if playing vs AI
        self.ai_turn = False  # True while AI is animating
        self._show_menu()

    # ── Mode Selection Screen ─────────────────────────────────────────────────
    def _show_menu(self):
        # Destroy game frames if they exist
        for w in self.winfo_children():
            w.destroy()

        self.game.reset()
        self.ai = None
        self.ai_turn = False

        menu = tk.Frame(self, bg=BG, padx=50, pady=40)
        menu.pack(expand=True)

        tk.Label(menu, text="🎲", bg=BG, fg=TEXT, font=("Courier New", 48)).pack(pady=(0, 4))
        tk.Label(menu, text="YAHTZEE", bg=BG, fg=ACCENT, font=("Courier New", 32, "bold")).pack()
        tk.Label(menu, text="Choose a game mode", bg=BG, fg=MUTED, font=("Courier New", 11)).pack(
            pady=(4, 28)
        )

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
            text="👥  2 Players (Local)",
            command=lambda: self._start_game("local"),
            highlightbackground="#58a6ff",
            bg="#58a6ff",
            activebackground="#3a8ae0",
            **btn_common,
        )
        b1.pack(pady=5)

        b2 = tk.Button(
            menu,
            text="🤖  vs AI (Easy)",
            command=lambda: self._start_game("ai_easy"),
            highlightbackground="#3fb950",
            bg="#3fb950",
            activebackground="#2ea043",
            **btn_common,
        )
        b2.pack(pady=5)

        b3 = tk.Button(
            menu,
            text="🧠  vs AI (Hard)",
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
            self.game.player_names = ["Player 1", "Player 2"]
            self.ai = None
        elif mode == "ai_easy":
            self.game.player_names = ["You", "AI (Easy)"]
            self.ai = AIPlayer("easy")
        elif mode == "ai_hard":
            self.game.player_names = ["You", "AI (Hard)"]
            self.ai = AIPlayer("hard")

        # Destroy menu and build game UI
        for w in self.winfo_children():
            w.destroy()
        self._build_ui()
        self._refresh()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        left = tk.Frame(self, bg=BG, padx=20, pady=20)
        right = tk.Frame(self, bg=PANEL, padx=18, pady=18)
        left.grid(row=0, column=0, sticky="nsew")
        right.grid(row=0, column=1, sticky="nsew")

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
            text="🎲   ROLL DICE",
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
            text="↺  NEW GAME",
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
        nl = tk.Label(
            row, text=cat, bg=PANEL, fg=TEXT, font=("Courier New", 9), width=16, anchor="w"
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

        # Attach tooltip only to the category name label
        if cat in CATEGORY_HINTS:
            Tooltip(nl, CATEGORY_HINTS[cat])

    def _hover_enter(self, row):
        # Cancel any pending leave
        if row._leave_id:
            self.after_cancel(row._leave_id)
            row._leave_id = None
        self._set_hover(row, True)

    def _hover_leave(self, row):
        # Delay unhighlight so moving between children in the same row
        # doesn't cause flickering
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
            self.game.roll()
            self._refresh()

    def _toggle_hold(self, idx):
        if self.ai_turn:
            return
        if self.game.rolls_left == MAX_ROLLS:
            return
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
        g.assign(cat)
        self._refresh()
        if g.game_over:
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
            g.assign(cat)
        self.ai_turn = False
        self._refresh()
        if g.game_over:
            self._end_game()

    # ── Rendering ─────────────────────────────────────────────────────────────
    def _refresh(self):
        g = self.game
        p = g.current
        clr = P1_CLR if p == 0 else P2_CLR

        # Turn indicator
        if g.game_over:
            self.turn_lbl.config(text="Game Over!", fg=GOLD)
        elif self.ai_turn:
            self.turn_lbl.config(text=f"🤖 {g.current_name} is thinking…", fg=P2_CLR)
        else:
            self.turn_lbl.config(text=f"▸ {g.current_name}'s Turn", fg=clr)

        rolls_str = "●" * g.rolls_left + "○" * (MAX_ROLLS - g.rolls_left)
        rnd = min(g.rounds[p], TOTAL_ROUNDS)
        self.info_lbl.config(text=f"Round {rnd}/{TOTAL_ROUNDS}   Rolls: {rolls_str}")
        can_roll = g.rolls_left > 0 and not g.game_over and not self.ai_turn
        self.roll_btn.config(
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
            self.upper_sub_lbls[p].config(text=f"  Upper sub : {us} / {UPPER_BONUS_THRESHOLD}")
            self.bonus_lbls[p].config(
                text=(
                    "  Bonus +35 : ✓ Earned!" if bonus else f"  Bonus +35 : need {remaining} more"
                )
            )
            self.total_lbls[p].config(text=f"  TOTAL : {g.total(p)}")

    def _update_hints(self):
        g = self.game
        p = g.current
        self.hint_box.config(state="normal")
        self.hint_box.delete("1.0", "end")
        if g.rolls_left < MAX_ROLLS and not g.game_over:
            rows = []
            for cat in ALL_CATS:
                if g.scores[p][cat] is None:
                    rows.append((g.potential(cat), cat))
            rows.sort(reverse=True)
            for pts, cat in rows:
                tag = "hi" if pts > 0 else "dim"
                self.hint_box.insert("end", f"  {cat:<22} {pts:>3}\n", tag)
        self.hint_box.config(state="disabled")

    def _end_game(self):
        g = self.game
        s0 = g.total(0)
        s1 = g.total(1)
        n0 = g.player_names[0]
        n1 = g.player_names[1]

        if s0 > s1:
            winner = f"🏆 {n0} wins!"
        elif s1 > s0:
            winner = f"🏆 {n1} wins!"
        else:
            winner = "🤝 It's a tie!"

        messagebox.showinfo("Game Over", f"{n0}: {s0}  |  {n1}: {s1}\n\n{winner}", parent=self)
