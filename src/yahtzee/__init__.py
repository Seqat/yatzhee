"""A 2-player Yahtzee dice game with a Tkinter GUI and AI opponents."""

__version__ = "0.1.0"


def main():
    from .ui.app import YahtzeeApp

    app = YahtzeeApp()
    app.mainloop()
