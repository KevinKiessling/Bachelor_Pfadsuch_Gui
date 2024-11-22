from tkinter import *
import math
class Pseudocode_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #to Access parent variables
        self.parent = parent

        #put the this frame on screen
        self.pack(pady=20)