
'''

Ausführen der Gui via : " pythonpfadsuche.py  "

'''
from gui.Main_Frame import PfadsuchApp
import tkinter as tk


def main():
    """
    Haupeinstigspunkt der GUI
    :return:
    """

    pfadsuch_app = PfadsuchApp()
    pfadsuch_app.mainloop()


if __name__ == "__main__":
    main()
