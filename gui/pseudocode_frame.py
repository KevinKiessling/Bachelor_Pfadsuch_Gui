from tkinter import *
from tkinter import ttk
import math
class Pseudocode_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.grid(row=0, column=1, sticky="nsew")


        self.step_label = Label(self, text="Aktueller Schritt: ", font=("Arial", 12))
        self.step_label.grid(row=0, column=0, pady=5, sticky="ew", padx=10)


        self.pseudocode_display_frame = Frame(self)
        self.pseudocode_display_frame.grid(row=1, column=0, pady=0, sticky="ew", padx=10)

        self.pseudocode_display = Text(self.pseudocode_display_frame, wrap=WORD, height=28, width=60, takefocus=0)
        self.pseudocode_display.grid(row=0, column=0, sticky="nsew")
        self.pseudocode_display.config(state=DISABLED)
        self.pseudocode_display.config(
            font=("Courier New", self.parent.font_size),
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

        # Scrollbar for Pseudocode Display
        self.scrollbar_pseudocode = Scrollbar(self.pseudocode_display_frame, orient="vertical",
                                              command=self.pseudocode_display.yview)
        self.scrollbar_pseudocode.grid(row=0, column=1, sticky="ns")
        self.pseudocode_display.configure(yscrollcommand=self.scrollbar_pseudocode.set)

        # Configure grid for pseudocode display frame
        self.pseudocode_display_frame.grid_columnconfigure(0, weight=1)
        self.pseudocode_display_frame.grid_rowconfigure(0, weight=1)

        self.distance_table_label = Label(self, text="Aktuelle Distanzen", font=("Arial", 12))
        self.distance_table_label.grid(row=2, column=0, pady=0, sticky="ew", padx=10)


        self.distance_table_frame = Frame(self, height=200)
        self.distance_table_frame.grid(row=3, column=0, sticky="nsew", padx=10)


        self.distance_table = ttk.Treeview(self.distance_table_frame, columns=("Node", "Distance"), show="headings",
                                           height=5)
        self.distance_table.grid(row=0, column=0, sticky="nsew")
        self.distance_table.heading("Node", text="Knoten")
        self.distance_table.heading("Distance", text="Distanz")
        self.distance_table.column("Node", anchor=CENTER)
        self.distance_table.column("Distance", anchor=CENTER)


        self.scrollbar_distance = Scrollbar(self.distance_table_frame, orient="vertical",
                                            command=self.distance_table.yview)
        self.distance_table.configure(yscrollcommand=self.scrollbar_distance.set)
        self.scrollbar_distance.grid(row=0, column=1, sticky="ns")


        self.distance_table_frame.grid_columnconfigure(0, weight=1)
        self.distance_table_frame.grid_rowconfigure(0, weight=0)


        self.priority_queue_label = Label(self, text="Priority Queue", font=("Arial", 12))
        self.priority_queue_label.grid(row=4, column=0, pady=0, sticky="ew", padx=10)


        self.priority_queue_frame = Frame(self, height=200)
        self.priority_queue_frame.grid(row=5, column=0, sticky="nsew", padx=10)


        self.priority_queue_table = ttk.Treeview(self.priority_queue_frame, columns=("Node", "Priority"),
                                                 show="headings", height=5)
        self.priority_queue_table.grid(row=0, column=0, sticky="nsew")
        self.priority_queue_table.heading("Node", text="Knoten")
        self.priority_queue_table.heading("Priority", text="Priorität")
        self.priority_queue_table.column("Node", anchor=CENTER)
        self.priority_queue_table.column("Priority", anchor=CENTER)

        # Scrollbar
        self.scrollbar_priority = Scrollbar(self.priority_queue_frame, orient="vertical",
                                            command=self.priority_queue_table.yview)
        self.priority_queue_table.configure(yscrollcommand=self.scrollbar_priority.set)
        self.scrollbar_priority.grid(row=0, column=1, sticky="ns")


        self.priority_queue_frame.grid_columnconfigure(0, weight=1)
        self.priority_queue_frame.grid_rowconfigure(0, weight=0)

        self.pcode = ""
        self.set_algorithm(self.parent.selected_algorithm)
        self.set_code_field(self.pcode)


        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=10, uniform="row")
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0, minsize=200)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0, minsize=200)
        self.grid_rowconfigure(6, weight=0)

        self.grid_columnconfigure(0, weight=1, uniform="column")


        self.grid_rowconfigure(6, weight=1, uniform="row")
        self.grid_columnconfigure(1, weight=1)

    def update_font_size(self):
        self.pseudocode_display.config(font=("Courier New", self.parent.font_size))
    def update_priority_queue(self, pq):

        if self.parent.selected_algorithm in {"Dijkstra_PQ_lazy", "Dijkstra_PQ"}:
            self.priority_queue_label.config(text="Priority Queue")
            self.priority_queue_table.heading("Node", text="Knoten")
            self.priority_queue_table.heading("Priority", text="Priorität")
        elif self.parent.selected_algorithm == "Dijkstra_List":
            self.priority_queue_label.config(text="Liste")
            self.priority_queue_table.heading("Node", text="Knoten")
            self.priority_queue_table.heading("Priority", text="Distanz")


        for item in self.priority_queue_table.get_children():
            self.priority_queue_table.delete(item)


        for priority, node in pq:
            display_priority = "∞" if priority == float("inf") else priority
            self.priority_queue_table.insert("", "end", values=(node, display_priority))
    def set_code_field(self, pcode):
        if self.parent.debug:
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


        if algorithm == "Dijkstra_PQ_lazy":
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
        if algorithm == "Dijkstra_PQ":
            self.pcode = """ Pseudocode: Dijkstra mit Priority Queue
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
19:                 Bestimme Position i von v in H
20:                 H.delete(i)
21:                 d[v] ← d[u] + ω(u, v) 
22:                 H.insert((v, d[v])) 
23:             end if
24:         end if
25:     end for
26: end while
"""

        self.set_code_field(self.pcode)
    def set_step(self, steptype, calculation=None):
        self.step_label.config(text=f"Aktueller Schritt: {steptype}")
        #if calculation:
            #self.calculation_label.config(text=f"Berechnung: {calculation}")

    # zwischen funktion die je nach step type die zugehörige Line im Pseudocode gelb markiert
    def highlight(self, step):
        if self.parent.debug:
            print(step)
        #self.pseudocode_display.see(f"{x}.0") for putting x on view
        if self.parent.selected_algorithm == "Dijkstra_PQ_lazy":
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
                self.pseudocode_display.see(f"{21}.0")
            if step == "Algorithm Finished":
                self.clear_hightlight()
                self.set_step("Algorithmus abgeschlossen")
        if self.parent.selected_algorithm == "Dijkstra_PQ":
            if step == "Select Node":
                self.highlight_lines_with_dimming([10, 11, 12, 13, 14, 15, 16, 27])
                self.set_step("Wähle Knoten")
            if step == "Initialization":
                self.highlight_lines_with_dimming([3, 4, 5, 6, 7, 8, 9])
                self.set_step("Initialisierung")
            if step == "Compare Distance":
                self.highlight_lines_with_dimming([19, 24])
                self.set_step("Vergleiche Distanzen")
            if step == "Highlight Edge":
                self.highlight_lines_with_dimming([17, 18, 25, 26])
                self.set_step("Wähle neue Kante")
            if step == "Update Distance":
                self.highlight_lines_with_dimming([20, 21, 22, 23])
                self.set_step("Update Distanzen")
            if step == "Algorithm Finished":
                self.clear_hightlight()
                self.set_step("Algorithmus abgeschlossen")
        if self.parent.selected_algorithm == "Dijkstra_List":
            if step == "Select Node":
                self.highlight_lines_with_dimming([14, 15, 16, 17, 23])
                self.set_step("Wähle Knoten")
            if step == "Initialization":
                self.highlight_lines_with_dimming([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
                self.set_step("Initialisierung")
            if step == "Compare Distance":
                self.highlight_lines_with_dimming([20])
                self.set_step("Vergleiche Distanzen")
            if step == "Highlight Edge":
                self.highlight_lines_with_dimming([18, 19, 21, 22])
                self.set_step("Wähle neue Kante")
            if step == "Update Distance":
                self.highlight_lines_with_dimming([20])
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
