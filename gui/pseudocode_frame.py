from tkinter import *
from tkinter import ttk
import math
from tkinter import font
class Pseudocode_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.italic_map = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"
        )
        self.bold_map = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
        )
        self.grid(row=0, column=1, sticky="nsew")


        self.step_label = Label(self, text="Aktueller Schritt: ", font=("Arial", 12))
        self.step_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)


        self.pseudocode_display_frame = Frame(self)
        self.pseudocode_display_frame.grid(row=1, column=0, pady=5, sticky="nsew", padx=10)


        self.pseudocode_display = Text(self.pseudocode_display_frame, wrap=WORD, height=10, width=60, takefocus=0)
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


        self.scrollbar_pseudocode = Scrollbar(self.pseudocode_display_frame, orient="vertical",
                                              command=self.pseudocode_display.yview)
        self.scrollbar_pseudocode.grid(row=0, column=1, sticky="ns")
        self.pseudocode_display.configure(yscrollcommand=self.scrollbar_pseudocode.set)


        self.pseudocode_display_frame.grid_columnconfigure(0, weight=1)
        self.pseudocode_display_frame.grid_rowconfigure(0, weight=1)


        self.distance_table_label = Label(self, text="Aktuelle Distanzen", font=("Arial", 12))
        self.distance_table_label.grid(row=2, column=0, pady=5, sticky="ew", padx=10)


        self.distance_table_frame = Frame(self, bd=1, relief=SOLID)
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
        self.scrollbar_distance.grid(row=0, column=1, sticky="ns")
        self.distance_table.configure(yscrollcommand=self.scrollbar_distance.set)


        self.distance_table_frame.grid_columnconfigure(0, weight=1)
        self.distance_table_frame.grid_rowconfigure(0, weight=1)


        self.priority_queue_label = Label(self, text="Priority Queue", font=("Arial", 12))
        self.priority_queue_label.grid(row=4, column=0, pady=5, sticky="ew", padx=10)


        self.priority_queue_frame = Frame(self, bd=1, relief=SOLID)
        self.priority_queue_frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=(0, 5))


        self.priority_queue_table = ttk.Treeview(self.priority_queue_frame, columns=("Node", "Priority"),
                                                 show="headings", height=5)
        self.priority_queue_table.grid(row=0, column=0, sticky="nsew")
        self.priority_queue_table.heading("Node", text="Knoten")
        self.priority_queue_table.heading("Priority", text="Priorität")
        self.priority_queue_table.column("Node", anchor=CENTER)
        self.priority_queue_table.column("Priority", anchor=CENTER)


        self.scrollbar_priority = Scrollbar(self.priority_queue_frame, orient="vertical",
                                            command=self.priority_queue_table.yview)
        self.scrollbar_priority.grid(row=0, column=1, sticky="ns")
        self.priority_queue_table.configure(yscrollcommand=self.scrollbar_priority.set)


        self.priority_queue_frame.grid_columnconfigure(0, weight=1)
        self.priority_queue_frame.grid_rowconfigure(0, weight=1)


        self.pcode = ""
        self.set_algorithm(self.parent.selected_algorithm)



        self.grid_rowconfigure(0, weight=0)  # Step label row
        self.grid_rowconfigure(1, weight=1)  # Pseudocode display
        self.grid_rowconfigure(2, weight=0)  # Distance table label row
        self.grid_rowconfigure(3, weight=1, minsize=100)  # Distance table
        self.grid_rowconfigure(4, weight=0)  # Priority queue label row
        self.grid_rowconfigure(5, weight=1, minsize=100)  # Priority queue


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def update_font_size(self):
        self.pseudocode_display.config(font=("Courier New", self.parent.font_size))
        self.style_pseudocode_initial()
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


    # hightlighted die jeweilige Linie im Code, Multilines machen das aber etwas komisch, funktioniert aber soweit
    def highlight_lines_with_dimming(self, line_numbers):

        self.pseudocode_display.config(state=NORMAL)

        self.pseudocode_display.tag_remove("highlight", "1.0", END)
        #self.pseudocode_display.tag_configure("highlight", background="light green", foreground="black")
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
            self.pcode = ""
        elif algorithm == "Dijkstra_PQ_lazy":
            self.pcode = """1:DijkstraH(Gerichteter Graph G = (V, E),
    Gewichtsfunktion ω : E → N, Startknoten s ∈ V):
2:   foreach v ∈ V do discovered[v] ← false, d[v] ← ∞ 
3:   d[s] ← 0, Heap H ← 0, H.insert((s, d[s])) 
4:   while H.length() > 0 do 
5:      u ← H.extractMin() 
6:      if discovered[u] then continue else 
            discovered[u] ← true
7:      forall (u, v) ∈ E do 
8:          if not discovered[v] then 
9:              if d[v] > d[u] + ω(u, v) then 
10:                 d[v] ← d[u] + ω(u, v) 
11:                 H.insert((v, d[v]))"""
        elif algorithm == "Dijkstra_PQ":
            self.pcode = ""


        self.pseudocode_display.config(state=NORMAL)
        self.pseudocode_display.delete("1.0", "end")
        self.pseudocode_display.tag_delete("bold")
        self.pseudocode_display.insert("1.0", self.pcode)
        self.pseudocode_display.config(state=DISABLED)


        self.style_pseudocode_initial()

    #funktion um characters im pseudocode bold/italic zu setzen
    def style_pseudocode_initial(self):
        self.pseudocode_display.config(state=NORMAL)


        bold_font = font.Font(family="Courier New", size=self.parent.font_size, weight="bold")
        italic_font = font.Font(family="Courier New", size=self.parent.font_size, slant="italic")


        self.pseudocode_display.tag_config("bold", font=bold_font)
        self.pseudocode_display.tag_config("italic", font=italic_font)

        keywords_bold = {
            "foreach": "bold",
            "while": "bold",
            "if": "bold",
            "then": "bold",
            "else": "bold",
            "do": "bold",
            "forall": "bold",
            "not": "bold"
        }
        keywords_italic = {
            "gerichteter": "italic",
            "Graph": "italic",
            "G": "italic",
            "V": "italic",
            "E": "italic",
            "Gewichtsfunktion": "italic",
            "Startknoten s": "italic",
            "d[v]": "italic",
            "s, d[s]": "italic",
            "H": "italic",
            "u ←": "italic",
            "[u]": "italic",
            "continue": "italic",
            "true": "italic",
            "(u, v)": "italic",
            "d[u]": "italic",
            "v, d[v]": "italic",

        }

        for keyword, style in keywords_bold.items():
            start_idx = "1.0"
            while True:

                start_idx = self.pseudocode_display.search(keyword, start_idx, stopindex="end")
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(keyword)}c"
                self.pseudocode_display.tag_add(style, start_idx, end_idx)
                start_idx = end_idx

        # Apply italic styling
        for keyword, style in keywords_italic.items():
            start_idx = "1.0"
            while True:

                start_idx = self.pseudocode_display.search(keyword, start_idx, stopindex="end")
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(keyword)}c"
                self.pseudocode_display.tag_add(style, start_idx, end_idx)
                start_idx = end_idx


        self.pseudocode_display.config(state=DISABLED)


        ''' Hardcoded Backup
        self.pseudocode_display.config(state=NORMAL)

        selected_algorithm = self.parent.selected_algorithm
        if selected_algorithm == "Dijkstra_PQ_lazy":
            bold_font = font.Font(family="Courier New", size=self.parent.font_size, weight="bold")

            #styling the pseudocode with bold/
            self.pseudocode_display.tag_add("bold", "3.5", "3.12") # foreach
            self.pseudocode_display.tag_add("bold", "3.19", "3.21") # do

            self.pseudocode_display.tag_add("bold", "5.5", "5.10") # while
            self.pseudocode_display.tag_add("bold", "5.26", "5.28") # do

            self.pseudocode_display.tag_add("bold", "7.8", "7.10") # if
            self.pseudocode_display.tag_add("bold", "7.24", "7.29") # then
            self.pseudocode_display.tag_add("bold", "7.39", "7.43")  #else

            self.pseudocode_display.tag_add("bold", "9.8", "9.14")  # forall
            self.pseudocode_display.tag_add("bold", "9.26", "9.28")  # do

            self.pseudocode_display.tag_add("bold", "10.12", "10.18")  # if not
            self.pseudocode_display.tag_add("bold", "10.33", "10.38")  # then

            self.pseudocode_display.tag_add("bold", "11.16", "11.18")  #if
            self.pseudocode_display.tag_add("bold", "11.41", "11.45") # then

        self.pseudocode_display.tag_config("bold", font=bold_font)


        self.pseudocode_display.config(state=DISABLED)'''

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
            if step == "Initialize Node Distance":
                self.highlight_lines_with_dimming([5])
                self.set_step("Initialisiere Knoten Distanzen")
                self.pseudocode_display.see(f"{3}.0")
            if step == "Initialize Visited":
                self.highlight_lines_with_dimming([4])
                self.set_step("Initialisiere besuchte Knoten")
                self.pseudocode_display.see(f"{3}.0")
            if step == "Pick Node":
                self.highlight_lines_with_dimming([3, 6])
                #self.test_highlight_characters_with_dimming(highlight_ranges)
                self.set_step("Wähle Knoten")
            if step == "Set Start Node Distance":
                self.highlight_lines_with_dimming([7])
                self.set_step("Setze Distanz von Startknoten")
            if step == "Push Start Node to Priority Queue":
                self.highlight_lines_with_dimming([8, 9])
                self.set_step("Füge Startknoten dem Heap hinzu")
            if step == "Heap Pop":
                self.highlight_lines_with_dimming([11])
                self.set_step("Entferne das oberste Heap Element")
            if step == "Algorithm Finished":
                self.clear_hightlight()
                self.set_step("Algorithmus abgeschlossen")
            if step == "Visit Node":
                self.highlight_lines_with_dimming([14, 15, 16])
                self.set_step("Setzte Knoten als Besucht")
            if step == "Compare Distance":
                self.highlight_lines_with_dimming([19, 22])
                self.set_step("Vergleiche Distanz")
            if step == "Highlight Edge":
                self.highlight_lines_with_dimming([18, 23])
                self.set_step("Wähle Kante wobei Zielknoten nicht vorher besucht")
            if step == "Begin Outer Loop":
                self.highlight_lines_with_dimming([10, 25])
                self.set_step("Solange der Heap nicht leer is")
            if step == "Begin Inner Loop":
                self.highlight_lines_with_dimming([17, 24])
                self.set_step("Iteriere über alle ausgehenden Kanten")
            if step == "Update Distance":
                self.highlight_lines_with_dimming([20])
                self.set_step("Update Distanzen und Pushe neue Distanz auf Heap")
            if step == "Push to Heap":
                self.highlight_lines_with_dimming([21])
                self.set_step("Update Distanzen und Pushe neue Distanz auf Heap")
            if step == "Skip Visited Node":
                self.highlight_lines_with_dimming([12, 13])
                self.set_step("Überspringe bereits bearbeitete Knoten")
            if step == "Skip Visited Neighbor":
                self.highlight_lines_with_dimming([18, 23])
                self.set_step("Überspringe Kante zu bereits besuchten Knoten")
            if step == "Priority Queue Empty":
                self.highlight_lines_with_dimming([10, 25])
                self.set_step("Keine Elemente In Priority Queue übrig")

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

    # Highlighte bestimmte characters in display.
