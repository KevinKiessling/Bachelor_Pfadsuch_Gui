# main.py

#from gui.interface import create_interface
from gui.pfadsuch_app import PfadsuchApp
import tkinter as tk

# Main Funktion, Programm mit python pfadsuche.py starten
def main():

    pfadsuch_app = PfadsuchApp()
    pfadsuch_app.mainloop()


if __name__ == "__main__":
    main()
