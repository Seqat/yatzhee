"""Hover tooltip widget for tkinter."""

import tkinter as tk

from ..theme import TEXT


class Tooltip:
    """Hover tooltip for tkinter widgets with delayed show/hide."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self._show_id = None
        self._hide_id = None
        widget.bind("<Enter>", self._schedule_show, add="+")
        widget.bind("<Leave>", self._schedule_hide, add="+")

    def _schedule_show(self, event=None):
        if self._hide_id:
            self.widget.after_cancel(self._hide_id)
            self._hide_id = None
        if self.tip_window or self._show_id:
            return
        self._show_id = self.widget.after(200, lambda: self._show(event))

    def _show(self, event=None):
        self._show_id = None
        if self.tip_window:
            return
        # Position to the right of the widget, vertically centered
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 8
        y = self.widget.winfo_rooty()
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.configure(bg="#30363d")
        # Border effect
        border = tk.Frame(tw, bg="#484f58", padx=1, pady=1)
        border.pack(fill="both", expand=True)
        label = tk.Label(
            border,
            text=self.text,
            justify="left",
            bg="#30363d",
            fg=TEXT,
            relief="flat",
            font=("Courier New", 9),
            padx=10,
            pady=6,
            wraplength=280,
        )
        label.pack()
        self.tip_window = tw

    def _schedule_hide(self, event=None):
        if self._show_id:
            self.widget.after_cancel(self._show_id)
            self._show_id = None
        if self._hide_id:
            return
        self._hide_id = self.widget.after(100, self._hide)

    def _hide(self):
        self._hide_id = None
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
