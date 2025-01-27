from tkinter import *
from tkinter import ttk
import math
from tkinter import font
import random
class Pseudocode_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.highlighted_tags = []
        self.grid(row=0, column=1, sticky="nsew")
        self.priority_queue = {}

        self.highlight_node = None
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

        self.main_frame = Frame(self, bd=0, relief=SOLID)
        self.main_frame.grid(row=5, column=0, sticky="nsew", padx=10)


        ''' Remove the switch button for now and just have the Heap/list on a canvas
        self.toggle_button = Button(self.main_frame, text="Switch to Table", command=self.toggle_view)
        #self.toggle_button.pack(pady=10)'''


        self.canvas_frame = Frame(self.main_frame, bd=1, relief="solid")
        self.canvas = Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(expand=True, fill="both")
        self.canvas_frame.pack_forget()


        '''Remove table for now
        self.table_frame = Frame(self.main_frame, bd=1, relief="solid")
        self.table = ttk.Treeview(self.table_frame, columns=("Knoten", "Distance"), show="headings", height=10)
        self.table.heading("Knoten", text="Knoten")
        self.table.heading("Distance", text="Distance")
        self.table.pack(expand=True, fill="both")
        self.table_frame.pack_forget()  '''

        # Initialize with the canvas visible
        self.current_view = "canvas"
        #self.draw_priority_queue(self.priority_queue)
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Bind the configure event to adjust tree when resizing
        self.canvas.bind("<Configure>", self.on_resize)

        self.pcode = ""
        self.set_algorithm(self.parent.selected_algorithm)



        self.grid_rowconfigure(0, weight=0)  # Step label row
        self.grid_rowconfigure(1, weight=1)  # Pseudocode display
        self.grid_rowconfigure(2, weight=0)  # Distance table label row
        self.grid_rowconfigure(3, weight=1, minsize=100)  # Distance table
        self.grid_rowconfigure(4, weight=0)  # Priority queue label row
        self.grid_rowconfigure(5, weight=1, minsize=100)  # Heap/list canvas


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def update_font_size(self):
        self.pseudocode_display.config(font=("Courier New", self.parent.font_size))
        self.style_pseudocode_initial()
    def update_priority_queue(self, pq):
        self.draw_priority_queue(pq)

        '''Remove Table for now
        self.populate_table(pq)'''
        self.priority_queue = pq.copy()


    #highlighted die zu dem nodename gehöhrende Row in der Distance Tabelle
    def highlight_row(self, node_name):

        for item in self.distance_table.get_children():
            self.distance_table.item(item, tags=())


        for index, item in enumerate(self.distance_table.get_children()):
            row_values = self.distance_table.item(item, "values")
            if row_values[0] == node_name:
                self.distance_table.item(item, tags=("highlight",))

                self.distance_table.see(item)
                self.center_item_in_view(index)
                break


        self.distance_table.tag_configure("highlight", background="yellow", foreground="black")

    def center_item_in_view(self, index):

        children = self.distance_table.get_children()
        total_items = len(children)


        if total_items > 0:
            fraction = index / max(total_items - 1, 1)
            self.distance_table.yview_moveto(fraction - (1 / len(children) / 2))

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
7:      forall (u, v) ∈ E  do 
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
            " not ": "bold"
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


    def set_step(self, steptype, calculation=None):
        self.step_label.config(text=f"Aktueller Schritt: {steptype}")

    # zwischen funktion die je nach step type die zugehörige Line im Pseudocode gelb markiert
    def highlight(self, step):
        if not self.parent.current_step == -1:
            step_for_highlighting_table = self.parent.steps_finished_algorithm[self.parent.current_step]
        if step_for_highlighting_table:
            current_node = step_for_highlighting_table["current_node"]


        if self.parent.debug:
            print(step)
        #self.pseudocode_display.see(f"{x}.0") for putting x on view
        if self.parent.selected_algorithm == "Dijkstra_PQ_lazy":
            if step == "Initialize Node Distance":
                self.highlight_step("Initialize Node Distance")
                self.set_step("Initialisiere Knoten Distanzen")
                self.highlight_row(current_node)
                self.pseudocode_display.see(f"{3}.0")
            if step == "Initialize Visited":
                self.highlight_step("Initialize Visited")
                self.set_step("Initialisiere besuchte Knoten")
                self.pseudocode_display.see(f"{3}.0")
            if step == "Pick Node":
                self.highlight_step("Pick Node")
                self.set_step("Wähle Knoten")
            if step == "Set Start Node Distance":
                self.highlight_step("Set Start Node Distance")
                self.set_step("Setze Distanz von Startknoten")
                self.highlight_row(current_node)
            if step == "Push Start Node to Priority Queue":
                self.highlight_step("Push Start Node to Priority Queue")
                self.set_step("Füge Startknoten dem Heap hinzu")
            if step == "Heap Pop":
                self.highlight_step("Heap Pop")
                self.set_step("Entferne das oberste Heap Element")
            if step == "Algorithm Finished":
                self.highlight_step("Algorithm Finished")
                self.set_step("Algorithmus abgeschlossen")
            if step == "Visit Node":
                self.highlight_step("Visit Node")
                self.set_step("Setzte Knoten als Besucht")
            if step == "Compare Distance":
                self.highlight_step("Compare Distance")
                self.set_step("Vergleiche Distanz")
            if step == "Highlight Edge":
                self.highlight_step("Highlight Edge")
                self.set_step("Wähle Kante wobei Zielknoten nicht vorher besucht")
            if step == "Begin Outer Loop":
                self.highlight_step("Begin Outer Loop")
                self.set_step("Solange der Heap nicht leer is")
            if step == "Begin Inner Loop":
                self.highlight_step("Begin Inner Loop")
                self.set_step("Iteriere über alle ausgehenden Kanten")
            if step == "Update Distance":
                self.highlight_step("Update Distance")
                self.highlight_row(step_for_highlighting_table["neighbor"])
                self.set_step("Update Distanzen")
            if step == "Push to Heap":
                self.highlight_step("Push to Heap")
                self.set_step("Pushe neue Distanz auf Heap")
            if step == "Skip Visited Node":
                self.highlight_step("Skip Visited Node")
                self.set_step("Überspringe bereits bearbeitete Knoten")
            if step == "Skip Visited Neighbor":
                self.highlight_step("Skip Visited Neighbor")
                self.set_step("Überspringe Kante zu bereits besuchten Knoten")
            if step == "Priority Queue Empty":
                self.highlight_step("Priority Queue Empty")
                self.set_step("Keine Elemente In Priority Queue übrig")
            if step == "Check if visited":
                self.highlight_step("Check if visited")
                self.set_step("Prüfe ob Knoten bereits besucht wurde")

        #if self.parent.selected_algorithm == "Dijkstra_PQ":



        #if self.parent.selected_algorithm == "Dijkstra_List":



    # Löscht Tabelle
    def clear_table(self):
        for item in self.distance_table.get_children():
            self.distance_table.delete(item)




    # Tabelle mit aktuellen distanzen
    def update_distances(self, distances):
        for item in self.distance_table.get_children():
            self.distance_table.delete(item)
        for node, distance in distances.items():
            display_distance = "∞" if distance == float("inf") else distance
            self.distance_table.insert("", "end", values=(node, display_distance))

    def highlight_step(self, step_type):

        self.pseudocode_display.config(state=NORMAL)
        for tag in self.highlighted_tags:
            self.pseudocode_display.tag_remove(tag, "1.0", "end")
        self.highlighted_tags.clear()

        colors = {
            "discovered": "#ffcc99",
            "Heap": "#d2cd6f",
            "d_value": "#ff9966",
            "u": "#ccffcc",
            "v": "#ffccff",
            "current_node": "yellow",
            "discovered_false": "orange",
            "discovered_true": "#00ff40",
            "show_edge": "light grey"
        }


        highlight_color = colors.get(step_type, "yellow")

        if self.parent.selected_algorithm == "Dijkstra_PQ_lazy":
            if step_type == "Pick Node":
                self.highlight_specific_ranges([("3.13", "3.18")], colors.get("current_node"))
                self.highlight_specific_ranges([("3.5", "3.12"),("3.19", "3.21")], colors.get("show_edge"))
            elif step_type == "Initialize Visited":
                self.highlight_specific_ranges([("3.22", "3.43")], colors.get("discovered_false"))
            elif step_type == "Initialize Node Distance":
                self.highlight_specific_ranges([("3.45", "3.53")], colors.get("current_node"))
            elif step_type == "Set Start Node Distance":
                self.highlight_specific_ranges([("4.5", "4.13")], colors.get("current_node"))
            elif step_type == "Push Start Node to Priority Queue":
                self.highlight_specific_ranges([("4.15", "4.46")], colors.get("Heap"))
            elif step_type == "Begin Outer Loop":
                self.highlight_specific_ranges([("5.11", "5.25")], colors.get("Heap"))
                self.highlight_specific_ranges([("5.5", "5.10"),("5.26", "5.28")], colors.get("show_edge"))
            elif step_type == "Heap Pop":
                self.highlight_specific_ranges([("6.8", "6.26")], colors.get("current_node"))
            elif step_type == "Visit Node":
                self.highlight_specific_ranges([("7.39", "7.43")], colors.get("show_edge"))
                self.highlight_specific_ranges([("8.12", "8.32")], colors.get("discovered_true"))
            elif step_type == "Skip Visited Node":
                self.highlight_specific_ranges([("7.30", "7.38")], colors.get("discovered_true"))
                self.highlight_specific_ranges([("7.25", "7.29")], colors.get("show_edge"))
            elif step_type == "Begin Inner Loop":
                self.highlight_specific_ranges([("9.8", "9.14"),("9.27", "9.29")], colors.get("show_edge"))

                self.highlight_specific_ranges([("9.15", "9.26")], "#4ecdf8")
            elif step_type == "Highlight Edge":
                self.highlight_specific_ranges([("10.15", "10.32")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.12", "10.14"),("10.33", "10.37")], colors.get("show_edge"))
            elif step_type == "Compare Distance":
                self.highlight_specific_ranges([("11.41", "11.45"),("11.16", "11.18")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.33", "11.40")], "#4ecdf8") # Kante bleibt so
                self.highlight_specific_ranges([("11.26", "11.30")], "pink") # d[u]
                self.highlight_specific_ranges([("11.19", "11.23")], "violet") # d[v]
            elif step_type == "Update Distance":
                self.highlight_specific_ranges([("12.34", "12.41")], "#4ecdf8") # Kante bleibt so
                self.highlight_specific_ranges([("12.27", "12.31")], "pink") # d[u]
                self.highlight_specific_ranges([("12.20", "12.24")], "violet") # d[v]
            elif step_type == "Push to Heap":
                self.highlight_specific_ranges([("13.20", "13.39")], colors.get("Heap"))
            elif step_type == "Priority Queue Empty":
                self.highlight_specific_ranges([("5.11", "5.25")], colors.get("Heap"))
                self.highlight_specific_ranges([("5.5", "5.10"),("5.26", "5.28")], colors.get("show_edge"))
            elif step_type == "Check if visited":
                self.highlight_specific_ranges([("7.8", "7.10")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.11", "7.24")], colors.get("show_edge"))
            elif step_type == "Skip Visited Neighbor":
                self.highlight_specific_ranges([("10.15", "10.32")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.12", "10.14"), ("10.33", "10.37")], colors.get("show_edge"))




        self.pseudocode_display.config(state=DISABLED)

    def highlight_specific_ranges(self, ranges, color):

        for start, end in ranges:
            tag_name = f"highlight_{start}-{end}"
            self.pseudocode_display.tag_add(f"highlight_{start}-{end}", start, end)
            self.pseudocode_display.tag_config(f"highlight_{start}-{end}", background=color)
            self.highlighted_tags.append(tag_name)

    '''remove tableview
    def populate_table(self, priority_queue):
        # Clear the table first
        for row in self.table.get_children():
            self.table.delete(row)
        # Populate the table with current data
        for item in priority_queue:
            if item[0] == self.highlight_node:
                self.table.insert("", "end", values=item, tags="highlight")
            else:
                self.table.insert("", "end", values=item)
        self.table.tag_configure("highlight", background="yellow")'''

    def draw_priority_queue(self, priority_queue):
        self.canvas.delete("all")

        def draw_node(x, y, text, is_highlighted=False):
            radius = 30
            color = "yellow" if is_highlighted else "lightgrey"
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
            self.canvas.create_text(x, y, text=text, font=("Arial", 12), fill="black")
            return x, y

        def draw_tree(index, x, y, dx):
            if index >= len(priority_queue):
                return

            node = priority_queue[index]
            is_highlighted = node[0] == self.highlight_node
            x, y = draw_node(x, y, f"{node[1]}\n{node[0]}", is_highlighted)

            left_child_idx = 2 * index + 1
            right_child_idx = 2 * index + 2

            if left_child_idx < len(priority_queue):
                left_x, left_y = x - dx, y + 60
                self.canvas.create_line(x, y + 30, left_x, left_y - 30)
                draw_tree(left_child_idx, left_x, left_y, dx // 2)

            if right_child_idx < len(priority_queue):
                right_x, right_y = x + dx, y + 60
                self.canvas.create_line(x, y + 30, right_x, right_y - 30)
                draw_tree(right_child_idx, right_x, right_y, dx // 2)


        width = self.canvas.winfo_width()
        if width > 0:
            draw_tree(0, width // 2, 50, width // 4)


        #self.populate_table(priority_queue)

    def on_resize(self, event):

        if self.current_view == "canvas":

            self.draw_priority_queue(self.priority_queue)

    ''' remoe table
    def toggle_view(self):
        if self.current_view == "canvas":
            self.canvas_frame.pack_forget()  # Hide the canvas frame
            self.table_frame.pack(expand=True, fill="both", padx=10, pady=10)  # Show the table frame
            self.toggle_button.config(text="Switch to Tree")
            self.current_view = "table"
        else:
            self.table_frame.pack_forget()  # Hide the table frame
            self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)  # Show the canvas frame
            self.toggle_button.config(text="Switch to Table")
            self.current_view = "canvas"'''

    def setup_frames(self):

        self.canvas_frame.pack_propagate(False)
        #self.table_frame.pack_propagate(False)

        # Set the width and height for the frames
        self.canvas_frame.config(width=800, height=400)
        #self.table_frame.config(width=800, height=400)

