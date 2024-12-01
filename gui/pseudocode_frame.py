from tkinter import *
import math
class Pseudocode_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent


        self.grid(row=0, column=1)

        self.pseudocode_display = Text(self, wrap=WORD, height=26, width=60, takefocus=0)
        self.pseudocode_display.pack(pady=20, fill=BOTH, expand=True)
        self.pseudocode_display.config(state=DISABLED)
        self.pseudocode_display.config(
            font=("Courier New", 14),
            bg="#f4f4f4",
            fg="#333333",
            insertbackground="pink",
            bd=2,
            relief=SOLID,
            padx=10,
            pady=10,
        )
        self.pcode = ""
        self.set_algorithm(self.parent.selected_algorithm)
        self.set_code_field(self.pcode)




    def set_code_field(self, pcode):
        print("Setting Pcode")
        self.pseudocode_display.config(state=NORMAL)
        self.pseudocode_display.delete(1.0, END)
        self.pseudocode_display.insert(END, pcode)
        self.pseudocode_display.config(state=DISABLED)

    def set_algorithm(self, algorithm):
        if algorithm == "Dijkstra_List":
            self.pcode = """Pseudocode: Dijkstra mit Liste
Input: Gerichteter Graph G = (V, E), Gewichtsfunktion ω : E → N, Startknoten s ∈ V
2: for each v ∈ V do
3:      discovered[v] ← false 
4: end for
5: for each v ∈ V do 
6:      d(v) ← ∞ 
7: end for
8: d(s) ← 0 
9: L ← []
10: for each v ∈ V do 
11:     L.add(v) 
12: end for
13: while not L.empty() do 
14:     wähle u ∈ L mit kleinstem Wert d[u] 
15:     L.remove(u) 
16:     discovered[u] ← true 
17:     for each (u, v) ∈ E do 
18:         if not discovered[v] then
19:             d[v] ← min(d[v], d[u] + ω(u, v)) 
20:         end if
21:     end for
22: end while          
"""


        if algorithm == "Dijkstra_PQ":
            self.pcode = """ Pseudocode: Dijkstra mit Priority Queue(mit Lazy Deletion)
1: Input: Gerichteter Graph G = (V, E), Gewichtsfunktion w : E → N, Startknoten s ∈ V
2: for each v ∈ V do
3:      discovered[v] ← false 
4:      d[v] ← ∞ 
5: end for
6: d[s] ← 0
7: Erstelle einen leeren Heap H 
8: H.insert((s, d[s])) 
9: while H.length() > 0 do 
10:     u ← H.extractMin() 
11:     if discovered[u] then 
12:         continue
13:     else
14:         discovered[u] ← true 
15:     end if
16:     for each (u, v) ∈ E do 
17:         if not discovered[v] then 
18:             if d[v] > d[u] + w(u, v) then 
19:                 d[v] ← d[u] + w(u, v) 
20:                 H.insert((v, d[v])) 
21:             end if
22:         end if
23:     end for
24: end while
"""
        self.set_code_field(self.pcode)
    def set_step(self, steptype):
        print("setting step to :", steptype)
