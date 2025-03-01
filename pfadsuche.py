
'''

Ausführen der Gui via : "python pfadsuche.py"

'''
from gui.Main_Frame import PfadsuchApp
import tkinter as tk


def main():
    """
    Haupeinstiegspunkt der GUI
    :return:
    """

    pfadsuch_app = PfadsuchApp()
    pfadsuch_app.mainloop()


if __name__ == "__main__":
    main()
