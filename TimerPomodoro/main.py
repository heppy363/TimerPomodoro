"""
Pomodoro Timer Pro 2.0
=====================
Timer Pomodoro professionale con interfaccia moderna

Author: Pomodoro Timer Team
Version: 2.0
"""

import tkinter as tk
from ui import PomodoroUI


def main():
    """Entry point applicazione"""
    root = tk.Tk()
    app = PomodoroUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()