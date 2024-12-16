from tkinter import *
from tkinter import ttk
import math
class Pseudocode_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent


        self.grid(row=0, column=1)
        self.info_frame = Frame(self)
        self.info_frame.pack(pady=10, fill=X)
        self.step_label = Label(self, text="Aktueller Schritt: ", font=("Arial", 14))
        self.step_label.pack(pady=10)

        #self.calculation_label = Label(self.info_frame, text="Berechnung: ", font=("Arial", 14))
        #self.calculation_label.pack(side=LEFT, padx=5)
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
        self.pseudocode_display.tag_configure("highlight", background="#ffff00")
        self.pseudocode_display.tag_configure("dim", background="#f0f0f0")

        self.distance_table_label = Label(self, text="Aktuelle Distanzen", font=("Arial", 16))
        self.distance_table_label.pack(pady=10)

        self.distance_table = ttk.Treeview(self, columns=("Node", "Distance"), show="headings", height=10)
        self.distance_table.pack(fill=BOTH, expand=True)

        # Spaltenüberschriften
        self.distance_table.heading("Node", text="Knoten")
        self.distance_table.heading("Distance", text="Distanz")
        self.distance_table.column("Node", width=100, anchor=CENTER)
        self.distance_table.column("Distance", width=150, anchor=CENTER)
        self.pcode = ""
        self.set_algorithm(self.parent.selected_algorithm)
        self.set_code_field(self.pcode)




    def set_code_field(self, pcode):
        print("Setting Pcode")
        self.pseudocode_display.config(state=NORMAL)
        self.pseudocode_display.delete(1.0, END)
        self.pseudocode_display.insert(END, pcode)
        self.pseudocode_display.config(state=DISABLED)



    # hightlighted die jeweilige Linie im Code, Multilines machen das aber etwas komisch, funktioniert aber soweit
    def highlight_lines_with_dimming(self, line_numbers):

        self.pseudocode_display.config(state=NORMAL)

        self.pseudocode_display.tag_remove("highlight", "1.0", END)
        self.pseudocode_display.tag_remove("dim", "1.0", END)


        for line_number in line_numbers:
            if line_number <= 0:
                continue
            start = f"{line_number}.0"
            end = f"{line_number}.end"
            self.pseudocode_display.tag_add("highlight", start, end)


        total_lines = int(self.pseudocode_display.index('end-1c').split('.')[0])
        for i in range(1, total_lines + 1):
            if i not in line_numbers:
                start = f"{i}.0"
                end = f"{i}.end"
                self.pseudocode_display.tag_add("dim", start, end)

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
1: Input: Gerichteter Graph G = (V, E), Gewichtsfunktion ω : E → N, Startknoten s ∈ V
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
18:             if d[v] > d[u] + ω(u, v) then 
19:                 d[v] ← d[u] + ω(u, v) 
20:                 H.insert((v, d[v])) 
21:             end if
22:         end if
23:     end for
24: end while
"""
        self.set_code_field(self.pcode)
    def set_step(self, steptype, calculation=None):
        self.step_label.config(text=f"Aktueller Schritt: {steptype}")
        #if calculation:
            #self.calculation_label.config(text=f"Berechnung: {calculation}")

    # zwischen funktion die je nach step type die zugehörige Line im Pseudocode gelb markiert
    def highlight(self, step):
        print(step)

        if self.parent.selected_algorithm == "Dijkstra_PQ":
            if step == "Select Node":
                self.highlight_lines_with_dimming([10, 11, 12, 13, 14, 15, 16, 25])
                self.set_step("Wähle Knoten")
            if step == "Initialization":
                self.highlight_lines_with_dimming([3, 4, 5, 6, 7, 8, 9])
                self.set_step("Initialisierung")
            if step == "Compare Distance":
                self.highlight_lines_with_dimming([19, 22])
                self.set_step("Vergleiche Distanzen")
            if step == "Highlight Edge":
                self.highlight_lines_with_dimming([17, 18, 23, 24])
                self.set_step("Wähle neue Kante")
            if step == "Update Distance":
                self.highlight_lines_with_dimming([20, 21])
                self.set_step("Update Distanzen")
            if step == "Algorithm Finished":
                self.clear_hightlight()
                self.set_step("Algorithmus abgeschlossen")


    # Löscht Tabelle
    def clear_table(self):
        for item in self.distance_table.get_children():
            self.distance_table.delete(item)

    # entfernt highlighting
    def clear_hightlight(self):
        self.pseudocode_display.tag_remove("highlight", "1.0", END)
        self.pseudocode_display.tag_remove("dim", "1.0", END)

    # Tabelle mit aktuellen distanzen
    def update_distances(self, distances):
        for item in self.distance_table.get_children():
            self.distance_table.delete(item)
        for node, distance in distances.items():
            display_distance = "∞" if distance == float("inf") else distance
            self.distance_table.insert("", "end", values=(node, display_distance))
