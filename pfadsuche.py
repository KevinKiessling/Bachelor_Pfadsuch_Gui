
'''

Main Entry Point, navigate to the directory and run via: " python pfadsuche.py  "

'''
from gui.pfadsuch_app import PfadsuchApp
import tkinter as tk


def main():

    pfadsuch_app = PfadsuchApp()
    pfadsuch_app.mainloop()


if __name__ == "__main__":
    main()
