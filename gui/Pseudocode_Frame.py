from tkinter import *
from tkinter import ttk
import math
from tkinter import font
import random
class Pseudocode_Frame(Frame):
    """
    Rechte Hälfte der GUI
    """
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


        self.pseudocode_display = Text(self.pseudocode_display_frame, wrap=WORD, height=12, width=60, takefocus=0)
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
        self.pseudocode_display_frame.grid_propagate(False)
        self.pseudocode_display_frame.config(width=800, height=400)
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


        self.canvas_frame = Frame(self.main_frame, bd=1, relief="solid")
        self.canvas = Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(expand=True, fill="both")
        self.canvas_frame.pack_forget()


        self.current_view = "canvas"
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.node_size_pq = 30
        self.font_size_pq = 14

        self.node_size_pq_original = self.node_size_pq
        self.font_size_pq_original = self.font_size_pq

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
        self.animation_step = 0
        self.animation_active = False
        self.after_id = None


    def update_font_size(self):
        """
        Updated die Fontsize des Pseudocodes
        :return:
        """
        self.pseudocode_display.config(font=("Courier New", self.parent.font_size))
        self.style_pseudocode_initial()

    def draw_list(self, list_data, distances, highlight_node=None):
        """
        Zeichnet die Liste
        :param list_data: Listen data
        :param distances: Distanuen
        :param highlight_node: Zu highlightender Knoten
        :return:
        """
        self.canvas.delete("all")

        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        num_elements = len(list_data)

        if num_elements == 0:
            return

        cols = max(1, int(width // 70))
        rows = (num_elements + cols - 1) // cols

        element_width = width // cols
        element_height = height // rows

        for i, value in enumerate(list_data):
            row, col = divmod(i, cols)
            x1 = col * element_width
            y1 = row * element_height
            x2 = x1 + element_width
            y2 = y1 + element_height

            color = self.parent.color_heap if value == highlight_node else "light grey"

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            distance = distances.get(value, float('inf'))
            distance_text = str(distance) if distance != float('inf') else '∞'

            text = f"{value}\nd[{value}] = {distance_text}"

            font_size_height = element_height // 3
            font_size_width = element_width // 6

            font_size = max(6, min(font_size_height, font_size_width))

            if width < 400:
                font_size = max(4, font_size // 2)

            text_center_y = center_y
            self.canvas.create_text(
                center_x,
                text_center_y,
                text=text,
                font=("Arial", font_size),
                justify="center",
                width=element_width - 4,
            )

    # draws heap with highlighting
    def update_priority_queue(self, pq):
        """
        Updated die Visuelle Priorityqueue
        :param pq: priorityqueue die updated werden soll
        :return:
        """
        if not self.parent.current_step == -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]
            if self.parent.selected_algorithm == "Dijkstra_List":
                if step["step_type"] == "Add Node to List":
                    self.draw_list(pq, step["distances"],step["current_node"])
                elif step["step_type"] == "Find Min in List":
                    self.draw_list(pq, step["distances"],step["current_node"])
                else:
                    self.draw_list(pq, step["distances"])
                return
        if not self.parent.current_step == -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]

            if step["step_type"] == "Push Start Node to Priority Queue":

                '''dis = step["distances"].get(step["current_node"])
                node = step["current_node"]
                self.draw_priority_queue(pq, node, dis)'''
                tmp_node = step["current_node"]
                tmp_pq = self.parent.steps_finished_algorithm[self.parent.current_step - 1]["priority_queue"]

                distance = step["distances"][tmp_node]
                tmp_tuple = (distance, tmp_node)

                self.insert_animation(tmp_pq, tmp_tuple)
            elif step["step_type"] == "Push to Heap":
                '''dis = step["distances"].get(step["neighbor"])
                node = step["neighbor"]
                self.draw_priority_queue(pq, node, dis)'''
                tmp_node = step["neighbor"]
                tmp_pq = self.parent.steps_finished_algorithm[self.parent.current_step - 1]["priority_queue"]

                distance = step["distances"][tmp_node]
                tmp_tuple = (distance, tmp_node)

                self.insert_animation(tmp_pq, tmp_tuple)
            elif step["step_type"] == "Find Position in Heap":
                dis = step["distances"].get(step["neighbor"])
                node = step["neighbor"]
                self.draw_priority_queue(pq, node, dis)
            elif step["step_type"] == "Remove from Heap":
                print("remove animation")
                help_step = self.parent.steps_finished_algorithm[self.parent.current_step - 1]
                help_pq = help_step["priority_queue"]
                help_node_to_be_removed = help_step["neighbor"]
                self.remove_node_heapify_animation(help_pq, help_node_to_be_removed)
            elif step["step_type"] == "Heap Pop":

                if self.parent.steps_finished_algorithm and self.parent.current_step > 0:
                    help_step = self.parent.steps_finished_algorithm[self.parent.current_step - 1]
                    self.pop_min_animation(help_step["priority_queue"])
                else:
                    print("No steps available or invalid current_step.")
            else:
                self.draw_priority_queue(pq)
        else:
            self.draw_priority_queue(pq)

        self.priority_queue = pq.copy()


    #highlighted die zu dem nodename gehöhrende Row in der Distance Tabelle
    def highlight_row(self, node_name_1, node_name_2=None):
        """
        Highlighted 1 bzw. optional 2 Reihen in der Distanz tabelle
        :param node_name_1: 1. Reihe
        :param node_name_2: 2. Reihe
        :return:
        """

        for item in self.distance_table.get_children():
            self.distance_table.item(item, tags=())


        for index, item in enumerate(self.distance_table.get_children()):
            row_values = self.distance_table.item(item, "values")
            if row_values[0] == node_name_1:
                self.distance_table.item(item, tags=("highlight_1",))
                self.distance_table.see(item)
                self.center_item_in_view(index)
                break


        if node_name_2:
            for index, item in enumerate(self.distance_table.get_children()):
                row_values = self.distance_table.item(item, "values")
                if row_values[0] == node_name_2:
                    self.distance_table.item(item, tags=("highlight_2",))
                    self.distance_table.see(item)
                    self.center_item_in_view(index)
                    break


        self.distance_table.tag_configure("highlight_1", background=self.parent.color_default, foreground="black")
        self.distance_table.tag_configure("highlight_2", background=self.parent.color_d_v, foreground="black")


        if not self.parent.current_step == -1:
            step_var = self.parent.steps_finished_algorithm[self.parent.current_step]
            if step_var["step_type"] == "Update Distance" or step_var["step_type"] == "Compare Distance":
                self.distance_table.tag_configure("highlight_1", background=self.parent.color_default,
                                                  foreground="black")
                self.distance_table.tag_configure("highlight_2", background=self.parent.color_d_v, foreground="black")

    def center_item_in_view(self, index):
        """
        Setzt den Focus der Tabelle auf das zu highligtende Element
        :param index: Index der highlighted werden soll
        :return:
        """

        children = self.distance_table.get_children()
        total_items = len(children)


        if total_items > 0:
            fraction = index / max(total_items - 1, 1)
            self.distance_table.yview_moveto(fraction - (1 / len(children) / 2))

    #Setzt den Text für das Pseudocode display, je nach algorithmus
    def set_algorithm(self, algorithm):
        """
        Setzt den Pseudocode basierend auf Parameter
        :param algorithm: Algorithmus der gesetzt werden soll
        :return:
        """

        if algorithm == "Dijkstra_List":
            self.pcode = """1:DijkstraH(Gerichteter Graph G = (V, E),
    Gewichtsfunktion ω : E → N, Startknoten s ∈ V):
2:   foreach v ∈ V do discovered[v] ← false
3:   foreach v ∈ V do d(v) ← ∞ 
4:   d(s) ← 0, List L ← ()
5:   foreach v ∈ V do L.add(v)
6:   while not L.empty() do 
7:      wähle u ∈ L mit kleinstem Wert d[u]
8:      L.remove(u)
9:      discovered[u] ← true
10:     forall (u, v) ∈ E  do
11:         if not discovered[v] then
              d[v] ← min(d[v], d[u] + ω(u, v))"""

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
            self.pcode = """1:DijkstraH(Gerichteter Graph G = (V, E),
    Gewichtsfunktion ω : E → N, Startknoten s ∈ V):
2:   foreach v ∈ V do discovered[v] ← false, d[v] ← ∞ 
3:   d[s] ← 0, Heap H ← 0, H.insert((s, d[s])) 
4:   while H.length() > 0 do 
5:      u ← H.extractMin() 
6:      discovered[u] ← true            
7:      forall (u, v) ∈ E  do 
8:          if not discovered[v] then 
9:              if d[v] > d[u] + ω(u, v) then 
10:                 bestimme Position i von v in H, 
                    H.delete(i)
11:                 d[v] ← d[u] + ω(u, v) 
12:                 H.insert((v, d[v]))"""


        self.pseudocode_display.config(state=NORMAL)
        self.pseudocode_display.delete("1.0", "end")
        self.pseudocode_display.tag_delete("bold")
        self.pseudocode_display.insert("1.0", self.pcode)
        self.pseudocode_display.config(state=DISABLED)


        self.style_pseudocode_initial()

    #funktion um characters im pseudocode bold/italic zu setzen
    def style_pseudocode_initial(self):
        """
        Styled den Pseudocode, sodass er wie in der vorlesung aussieht
        :return:
        """
        self.pseudocode_display.config(state=NORMAL)


        bold_font = font.Font(family="Courier New", size=self.parent.font_size, weight="bold")
        italic_font = font.Font(family="Courier New", size=self.parent.font_size, slant="italic")
        infinity_font = font.Font(family="Courier New", size=self.parent.font_size+3)

        self.pseudocode_display.tag_config("infinity", font=infinity_font)
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
            "Gerichteter": "italic",
            "Graph": "italic",
            "G": "italic",
            "V": "italic",
            "E": "italic",
            "Gewichtsfunktion": "italic",
            "Startknoten s": "italic",
            "d[v]": "italic",
            "s, d[s]": "italic",
            "H.": "italic",
            "u ←": "italic",
            "[u]": "italic",
            "continue": "italic",
            "u, v": "italic",
            "d[u]": "italic",
            "v, d[v]": "italic",
            "d[s]": "italic",
            "H ←": "italic",
            "ω": "italic",
            " L ": "italic",
            "L.": "italic",
            "bestimme Position i von v in H": "italic",
            " v ": "italic"
        }
        keywords_infinity = {
            "∞": "infinity",
        }

        def apply_tag_to_keywords(keywords_dict):
            """
            Fügt den Keywords tags hinzu, wird fürs styling genutzt
            :param keywords_dict: Dictionary mit Keywords
            :return:
            """
            for keyword, style in keywords_dict.items():
                start_idx = "1.0"
                while start_idx:
                    start_idx = self.pseudocode_display.search(keyword, start_idx, stopindex="end")
                    if start_idx:
                        end_idx = f"{start_idx}+{len(keyword)}c"
                        self.pseudocode_display.tag_add(style, start_idx, end_idx)
                        start_idx = end_idx
                    else:
                        break


        apply_tag_to_keywords(keywords_bold)
        apply_tag_to_keywords(keywords_infinity)
        apply_tag_to_keywords(keywords_italic)


        self.pseudocode_display.config(state=DISABLED)


    def set_step(self, steptype, calculation=None):
        """
        Setzt das Label
        :param steptype: Aktueller schritt
        :param calculation:
        :return:
        """
        self.step_label.config(text=f"Aktueller Schritt: {steptype}")

    # zwischen funktion die je nach step type die zugehörige Line im Pseudocode gelb markiert
    def highlight(self, step):
        """
        Highlighted Linien um pseudocode
        :param step: akteuller schritt
        :return:
        """
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
                self.highlight_row(current_node, step_for_highlighting_table["neighbor"])
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
                self.highlight_row(current_node, step_for_highlighting_table["neighbor"])
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

        if self.parent.selected_algorithm == "Dijkstra_PQ":
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
                self.highlight_row(current_node, step_for_highlighting_table["neighbor"])
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
                self.highlight_row(current_node, step_for_highlighting_table["neighbor"])
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
            if step == "Find Position in Heap":
                self.highlight_step("Find Position in Heap")
                self.set_step("Finde Position i von v im Heap")
            if step == "Remove from Heap":
                self.highlight_step("Remove from Heap")
                self.set_step("Entferne Element an Position i aus dem Heap")


        if self.parent.selected_algorithm == "Dijkstra_List":
            if step == "Initialize Node Distance":
                self.highlight_step("Initialize Node Distance")
                self.set_step("Initialisiere Knoten Distanzen")
                self.highlight_row(current_node)
                self.pseudocode_display.see(f"{3}.0")
            if step == "Initialize Visited":
                self.highlight_step("Initialize Visited")
                self.set_step("Initialisiere besuchte Knoten")
                self.pseudocode_display.see(f"{3}.0")
            if step == "Pick Node_1":
                self.highlight_step("Pick Node_1")
                self.set_step("Wähle Knoten1")
            if step == "Pick Node_2":
                self.highlight_step("Pick Node_2")
                self.set_step("Wähle Knoten2")
            if step == "Pick Node_3":
                self.highlight_step("Pick Node_3")
                self.set_step("Wähle Knoten3")
            if step == "Set Start Node Distance":
                self.highlight_step("Set Start Node Distance")
                self.set_step("Setze Distanz von Startknoten")
                self.highlight_row(current_node)
            if step == "Initialize List":
                self.highlight_step("Initialize List")
                self.set_step("Initialize List")
            if step == "Add Node to List":
                self.highlight_step("Add Node to List")
                self.set_step("Add Node to List")
            if step == "Algorithm Finished":
                self.highlight_step("Algorithm Finished")
                self.set_step("Algorithmus abgeschlossen")
            if step == "Visit Node":
                self.highlight_step("Visit Node")
                self.set_step("Setzte Knoten als Besucht")
            if step == "Compare Distance":
                self.highlight_step("Compare Distance")
                self.highlight_row(current_node, step_for_highlighting_table["neighbor"])
                self.set_step("Vergleiche Distanz")
            if step == "Highlight Edge":
                self.highlight_step("Highlight Edge")
                self.set_step("Wähle Kante wobei Zielknoten nicht vorher besucht")
            if step == "Begin Outer Loop":
                self.highlight_step("Begin Outer Loop")
                self.set_step("Solange die Liste nicht leer is")
            if step == "Begin Inner Loop":
                self.highlight_step("Begin Inner Loop")
                self.set_step("Iteriere über alle ausgehenden Kanten")
            if step == "Update Distance":
                self.highlight_step("Update Distance")
                self.highlight_row(current_node, step_for_highlighting_table["neighbor"])
                self.set_step("Update Distanzen")
            if step == "Find Min in List":
                self.highlight_step("Find Min in List")
                self.set_step("Find Min in List")
            if step == "Skip Visited Node":
                self.highlight_step("Skip Visited Node")
                self.set_step("Überspringe bereits bearbeitete Knoten")
            if step == "Skip Visited Neighbor":
                self.highlight_step("Skip Visited Neighbor")
                self.set_step("Überspringe Kante zu bereits besuchten Knoten")
            if step == "Remove min from List":
                self.highlight_step("Remove min from List")
                self.set_step("Remove min from List")
            if step == "Check if visited":
                self.highlight_step("Check if visited")
                self.set_step("Prüfe ob Knoten bereits besucht wurde")
            if step == "Visit Node u ":
                self.highlight_step("Visit Node u ")
                self.set_step("Visit Node u ")
            if step == "List Empty":
                self.highlight_step("List Empty")
                self.set_step("List Empty")


        #if self.parent.selected_algorithm == "Dijkstra_List":

    def clear_highlights_and_Canvas(self):
        """
        Setzt alle highlights zurück
        :return:
        """
        # Iterate through all rows and remove any tags
        for item in self.distance_table.get_children():
            self.distance_table.item(item, tags=())  # Remove all tags
        self.pseudocode_display.config(state=NORMAL)
        for tag in self.highlighted_tags:
            self.pseudocode_display.tag_remove(tag, "1.0", "end")
        self.pseudocode_display.config(state=DISABLED)
        self.canvas.delete("all")

    # Löscht Tabelle
    def clear_table(self):
        """
        Löscht die Tabelle
        :return:
        """
        for item in self.distance_table.get_children():
            self.distance_table.delete(item)




    # Tabelle mit aktuellen distanzen
    def update_distances(self, distances):
        """
        Füllt die Tabelle mit neuen Distanzen
        :param distances: Distance liste
        :return:
        """
        for item in self.distance_table.get_children():
            self.distance_table.delete(item)
        for node, distance in distances.items():
            display_distance = "∞" if distance == float("inf") else distance
            self.distance_table.insert("", "end", values=(node, display_distance))

    def highlight_step(self, step_type):
        """
        Highlighted schritt im Pseudocode, basierend auf schritttyp und ausgewähltem Algorithmus
        :param step_type: Schritt typ
        :return:
        """

        self.pseudocode_display.config(state=NORMAL)
        for tag in self.highlighted_tags:
            self.pseudocode_display.tag_remove(tag, "1.0", "end")
        self.highlighted_tags.clear()

        colors = {
            "Heap": self.parent.color_heap,
            "current_node": self.parent.color_default,
            "discovered_false": self.parent.color_discovered_false,
            "discovered_true": self.parent.color_discovered_true,
            "d_v": self.parent.color_d_v,
            "show_edge": "light grey",
            "highlighted_edge": self.parent.color_edge_highlight
        }


        highlight_color = colors.get(step_type, "yellow")

        if self.parent.selected_algorithm == "Dijkstra_PQ_lazy":
            if step_type == "Starting Algorithm":
                self.highlight_specific_ranges([("1.2", "1.42")], colors.get("show_edge"))
                self.highlight_specific_ranges([("2.4", "2.52")], colors.get("show_edge"))
            if step_type == "Pick Node":
                self.highlight_specific_ranges([("3.13", "3.18")], colors.get("current_node"))
                self.highlight_specific_ranges([("3.5", "3.12")], colors.get("show_edge"))

            elif step_type == "Initialize Visited":
                self.highlight_specific_ranges([("3.22", "3.43")], colors.get("discovered_false"))
                self.highlight_specific_ranges([("3.19", "3.21")], colors.get("show_edge"))
            elif step_type == "Initialize Node Distance":
                self.highlight_specific_ranges([("3.45", "3.53")], colors.get("current_node"))
                self.highlight_specific_ranges([("3.19", "3.21")], colors.get("show_edge"))
            elif step_type == "Set Start Node Distance":
                self.highlight_specific_ranges([("4.5", "4.13")], colors.get("current_node"))
            elif step_type == "Push Start Node to Priority Queue":
                self.highlight_specific_ranges([("4.15", "4.46")], colors.get("Heap"))
            elif step_type == "Begin Outer Loop":
                self.highlight_specific_ranges([("5.11", "5.25")], colors.get("Heap"))
                self.highlight_specific_ranges([("5.5", "5.10")], colors.get("show_edge"))
               # self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
            elif step_type == "Heap Pop":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("6.8", "6.26")], colors.get("current_node"))
            elif step_type == "Visit Node":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.39", "7.43")], colors.get("show_edge"))
                self.highlight_specific_ranges([("8.12", "8.32")], colors.get("discovered_true"))
            elif step_type == "Skip Visited Node":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.30", "7.38")], colors.get("discovered_true"))
                self.highlight_specific_ranges([("7.25", "7.29")], colors.get("show_edge"))
            elif step_type == "Begin Inner Loop":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("9.8", "9.14")], colors.get("show_edge"))
                #self.highlight_specific_ranges([("9.27", "9.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("9.15", "9.26")], colors.get("highlighted_edge"))
            elif step_type == "Highlight Edge":
                self.highlight_specific_ranges([("9.27", "9.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.15", "10.32")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.12", "10.14")], colors.get("show_edge"))
            elif step_type == "Compare Distance":
                self.highlight_specific_ranges([("9.27", "9.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.16", "11.18"),("10.33", "10.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.33", "11.40")], colors.get("highlighted_edge")) # Kante bleibt so
                self.highlight_specific_ranges([("11.26", "11.30")], colors.get("current_node")) # d[u]
                self.highlight_specific_ranges([("11.19", "11.23")], colors.get("d_v")) # d[v]
            elif step_type == "Update Distance":
                self.highlight_specific_ranges([("9.27", "9.29"),("10.33", "10.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.41", "11.45")], colors.get("show_edge"))
                self.highlight_specific_ranges([("12.34", "12.41")], colors.get("highlighted_edge")) # Kante bleibt so
                self.highlight_specific_ranges([("12.27", "12.31")], colors.get("current_node")) # d[u]
                self.highlight_specific_ranges([("12.20", "12.24")], colors.get("d_v")) # d[v]
            elif step_type == "Push to Heap":
                self.highlight_specific_ranges([("9.27", "9.29"),("10.33", "10.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.41", "11.45")], colors.get("show_edge"))
                self.highlight_specific_ranges([("13.20", "13.39")], colors.get("Heap"))
            elif step_type == "Priority Queue Empty":
                self.highlight_specific_ranges([("5.11", "5.25")], colors.get("Heap"))
                self.highlight_specific_ranges([("5.5", "5.10"),("5.26", "5.28")], colors.get("show_edge"))
            elif step_type == "Check if visited":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.8", "7.10")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.11", "7.24")], colors.get("show_edge"))
            elif step_type == "Skip Visited Neighbor":
                self.highlight_specific_ranges([("5.26", "5.28"),("9.27", "9.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.15", "10.32")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.12", "10.14")], colors.get("show_edge"))

        if self.parent.selected_algorithm == "Dijkstra_PQ":
            if step_type == "Starting Algorithm":
                self.highlight_specific_ranges([("1.2", "1.42")], colors.get("show_edge"))
                self.highlight_specific_ranges([("2.4", "2.52")], colors.get("show_edge"))
            if step_type == "Pick Node":
                self.highlight_specific_ranges([("3.13", "3.18")], colors.get("current_node"))
                self.highlight_specific_ranges([("3.5", "3.12")], colors.get("show_edge"))

            elif step_type == "Initialize Visited":
                self.highlight_specific_ranges([("3.19", "3.21")], colors.get("show_edge"))  # do line 1
                self.highlight_specific_ranges([("3.22", "3.43")], colors.get("discovered_false"))
            elif step_type == "Initialize Node Distance":
                self.highlight_specific_ranges([("3.19", "3.21")], colors.get("show_edge"))  # do line 1
                self.highlight_specific_ranges([("3.45", "3.53")], colors.get("current_node"))
            elif step_type == "Set Start Node Distance":
                self.highlight_specific_ranges([("4.5", "4.13")], colors.get("current_node"))
            elif step_type == "Push Start Node to Priority Queue":
                self.highlight_specific_ranges([("4.15", "4.46")], colors.get("Heap"))
            elif step_type == "Begin Outer Loop":
                self.highlight_specific_ranges([("5.11", "5.25")], colors.get("Heap"))
                self.highlight_specific_ranges([("5.5", "5.10")], colors.get("show_edge"))

            elif step_type == "Heap Pop":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("6.8", "6.26")], colors.get("current_node"))
            elif step_type == "Visit Node":
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("7.8", "7.28")], colors.get("discovered_true"))
            elif step_type == "Begin Inner Loop":
                self.highlight_specific_ranges([("8.8", "8.14")], colors.get("show_edge"))

                self.highlight_specific_ranges([("8.15", "8.26")], colors.get("highlighted_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
            elif step_type == "Highlight Edge":
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("9.15", "9.32"),("9.12", "9.14")], colors.get("show_edge"))
            elif step_type == "Compare Distance":
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("10.16", "10.18"),("9.33", "9.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.33", "10.40")], colors.get("highlighted_edge")) # Kante bleibt so
                self.highlight_specific_ranges([("10.26", "10.30")], colors.get("current_node")) # d[u]
                self.highlight_specific_ranges([("10.19", "10.23")], colors.get("d_v")) # d[v]

            elif step_type == "Find Position in Heap":
                self.highlight_specific_ranges([("9.33", "9.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("10.41", "10.45")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.20", "11.51")], colors.get("Heap"))

            elif step_type == "Remove from Heap":
                self.highlight_specific_ranges([("9.33", "9.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("10.41", "10.45")], colors.get("show_edge"))
                self.highlight_specific_ranges([("12.20", "12.32")], colors.get("Heap"))

            elif step_type == "Update Distance":
                self.highlight_specific_ranges([("9.33", "9.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("10.41", "10.45")], colors.get("show_edge"))
                self.highlight_specific_ranges([("13.34", "13.41")], colors.get("highlighted_edge")) # Kante bleibt so
                self.highlight_specific_ranges([("13.27", "13.31")], colors.get("current_node")) # d[u]
                self.highlight_specific_ranges([("13.20", "13.24")], colors.get("d_v")) # d[v]

            elif step_type == "Push to Heap":
                self.highlight_specific_ranges([("9.33", "9.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("10.41", "10.45")], colors.get("show_edge"))
                self.highlight_specific_ranges([("14.20", "14.39")], colors.get("Heap"))

            elif step_type == "Priority Queue Empty":
                self.highlight_specific_ranges([("5.11", "5.25")], colors.get("Heap"))
                self.highlight_specific_ranges([("5.5", "5.10")], colors.get("show_edge"))

            elif step_type == "Skip Visited Neighbor":
                self.highlight_specific_ranges([("8.27", "8.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("9.15", "9.32")], colors.get("show_edge"))
                self.highlight_specific_ranges([("5.26", "5.28")], colors.get("show_edge"))  # do while
                self.highlight_specific_ranges([("9.12", "9.14")], colors.get("show_edge"))


        if self.parent.selected_algorithm == "Dijkstra_List":
            if step_type == "Starting Algorithm":
                self.highlight_specific_ranges([("1.2", "1.42")], colors.get("show_edge"))
                self.highlight_specific_ranges([("2.4", "2.52")], colors.get("show_edge"))
            if step_type == "Pick Node_1":
                self.highlight_specific_ranges([("3.13", "3.18")], colors.get("current_node"))
                self.highlight_specific_ranges([("3.5", "3.12")], colors.get("show_edge"))
            if step_type == "Pick Node_2":
                self.highlight_specific_ranges([("4.13", "4.18")], colors.get("current_node"))
                self.highlight_specific_ranges([("4.5", "4.12")], colors.get("show_edge"))
            if step_type == "Pick Node_3":
                self.highlight_specific_ranges([("6.13", "6.18")], colors.get("current_node"))
                self.highlight_specific_ranges([("6.5", "6.12")], colors.get("show_edge"))
            elif step_type == "Initialize Visited":
                self.highlight_specific_ranges([("3.19", "3.21")], colors.get("show_edge"))
                self.highlight_specific_ranges([("3.22", "3.43")], colors.get("discovered_false"))
            elif step_type == "Initialize Node Distance":
                self.highlight_specific_ranges([("4.19", "4.21")], colors.get("show_edge"))
                self.highlight_specific_ranges([("4.22", "4.30")], colors.get("current_node"))

            elif step_type == "Set Start Node Distance":
                self.highlight_specific_ranges([("5.5", "5.13")], colors.get("current_node"))

            elif step_type == "Begin Outer Loop":
                self.highlight_specific_ranges([("7.15", "7.24")], colors.get("Heap"))
                self.highlight_specific_ranges([("7.5", "7.14")], colors.get("show_edge"))
            elif step_type == "List Empty":
                self.highlight_specific_ranges([("7.15", "7.24")], colors.get("Heap"))
                self.highlight_specific_ranges([("7.5", "7.14")], colors.get("show_edge"))

            elif step_type == "Visit Node":
                self.highlight_specific_ranges([("7.8", "7.28")], colors.get("discovered_true"))
            elif step_type == "Begin Inner Loop":
                self.highlight_specific_ranges([("7.25", "7.27")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.8", "11.14")], colors.get("show_edge"))
                self.highlight_specific_ranges([("11.15", "11.26")], colors.get("highlighted_edge"))
            elif step_type == "Highlight Edge":
                self.highlight_specific_ranges([("12.15", "12.32"),("12.12", "12.14"),("11.27", "11.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.25", "7.27")], colors.get("show_edge"))

            elif step_type == "Compare Distance":
                self.highlight_specific_ranges([("10.16", "10.18"),("9.33", "9.37")], colors.get("show_edge"))
                self.highlight_specific_ranges([("10.33", "10.40")], colors.get("highlighted_edge")) # Kante bleibt so
                self.highlight_specific_ranges([("10.26", "10.30")], colors.get("current_node")) # d[u]
                self.highlight_specific_ranges([("10.19", "10.23")], colors.get("d_v")) # d[v]
            elif step_type == "Initialize List":

                self.highlight_specific_ranges([("5.15", "5.26")], colors.get("Heap"))

            elif step_type == "Add Node to List":
                self.highlight_specific_ranges([("6.19", "6.21")], colors.get("show_edge"))
                self.highlight_specific_ranges([("6.22", "6.32")], colors.get("Heap"))

            elif step_type == "Update Distance":
                self.highlight_specific_ranges([("12.33", "12.41"),("11.27", "11.29")], colors.get("show_edge"))
                self.highlight_specific_ranges([("13.38", "13.45")], colors.get("highlighted_edge")) # Kante bleibt so
                self.highlight_specific_ranges([("13.31", "13.35")], colors.get("current_node")) # d[u]
                self.highlight_specific_ranges([("13.14", "13.18"),("13.25", "13.29")], colors.get("d_v")) # d[v]
                self.highlight_specific_ranges([("7.25", "7.27")], colors.get("show_edge"))

            elif step_type == "Skip Visited Neighbor":
                self.highlight_specific_ranges([("12.15", "12.32")], colors.get("show_edge"))
                self.highlight_specific_ranges([("12.12", "12.14")], colors.get("show_edge"))
                self.highlight_specific_ranges([("7.25", "7.27"),("11.27", "11.29")], colors.get("show_edge"))

            elif step_type == "Find Min in List":
                self.highlight_specific_ranges([("7.25", "7.27")], colors.get("show_edge")) # do
                self.highlight_specific_ranges([("8.8", "8.43")], colors.get("Heap"))
            elif step_type == "Remove min from List":
                self.highlight_specific_ranges([("7.25", "7.27")], colors.get("show_edge")) # do
                self.highlight_specific_ranges([("9.8", "9.20")], colors.get("Heap"))
            elif step_type == "Visit Node u ":
                self.highlight_specific_ranges([("7.25", "7.27")], colors.get("show_edge")) # do
                self.highlight_specific_ranges([("10.8", "10.30")], colors.get("discovered_true"))
    #,("11.27", "11.29")




        self.pseudocode_display.config(state=DISABLED)

    def highlight_specific_ranges(self, ranges, color):
        """
        Highlighted die Zeichen innerhalb der Ranges in der Color
        :param ranges: zu highlightender Bereicht
        :param color: Farbe
        :return:
        """

        for start, end in ranges:
            tag_name = f"highlight_{start}-{end}"
            self.pseudocode_display.tag_add(f"highlight_{start}-{end}", start, end)
            self.pseudocode_display.tag_config(f"highlight_{start}-{end}", background=color)
            self.highlighted_tags.append(tag_name)




    def on_resize(self, event=None):
        """
        Skalierungsfunktion für die Liste und Priority Queue
        :param event: Resize event
        :return:
        """

        if self.parent.selected_algorithm == "Dijkstra_PQ_lazy" or self.parent.selected_algorithm == "Dijkstra_PQ":
            if self.parent.steps_finished_algorithm:
                step = self.parent.steps_finished_algorithm[self.parent.current_step]
                if step["step_type"] not in {"Heap Pop", "Push to Heap"}:
                    self.draw_priority_queue(self.priority_queue)
        else:
            if self.parent.current_step == -1:
                return
            else:

                step = self.parent.steps_finished_algorithm[self.parent.current_step]
                list_var = step["list"]
                self.draw_list(list_var, step["distances"])

    def draw_priority_queue(self, priority_queue, highlight_node=None, highlight_distance=None):
        """
        Zeichnet die priority Queue als Baum, mit optionalem Highlighting
        :param priority_queue: Priority Queue
        :param highlight_node: optionales Highlight
        :param highlight_distance: optionales Highlight
        :return:
        """
        self.canvas.delete("all")

        if not priority_queue:
            return

        num_levels = math.floor(math.log2(len(priority_queue))) + 1

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        nodes_on_widest_level = 2 ** (num_levels - 1)

        node_size_x = canvas_width / (nodes_on_widest_level * 2)
        node_size_y = canvas_height / (num_levels * 3)

        node_size = min(min(node_size_x, node_size_y), 35)

        self.node_size_pq = node_size
        self.font_size_pq = max(1, int(node_size // 2))

        horizontal_spacing = canvas_width / (2 ** num_levels)
        vertical_spacing = canvas_height / (num_levels + 1)

        def draw_node(x, y, text, is_highlighted=False):
            """
            Zeichnet einen Knoten
            :param x: x Koordinate
            :param y: y Koordinate
            :param text: Beschriftung
            :param is_highlighted: Highlighting, yes/no
            :return:
            """
            color = self.parent.color_heap if is_highlighted else "lightgrey"
            self.canvas.create_oval(
                x - node_size, y - node_size, x + node_size, y + node_size, fill=color
            )
            # Only draw the text if the node is not "empty"
            if text != "empty":
                self.canvas.create_text(x, y, text=text, font=("Arial", self.font_size_pq), fill="black")

        def draw_tree(index, x, y, dx):
            """
            Zeichnet rekursiv den Binärbaum
            :param index: aktueller index
            :param x: x Koordinate
            :param y: y Koordinate
            :param dx: Offet
            :return:
            """
            if index >= len(priority_queue):
                return

            node = priority_queue[index]
            is_highlighted = (
                    (highlight_node is not None and node[1] == highlight_node)
                    and (highlight_distance is not None and node[0] == highlight_distance)
            )

            # If the node is empty, display an empty label without text
            if node[1] is None:
                draw_node(x, y, "empty", is_highlighted)
            else:
                draw_node(x, y, f"{node[1]}, {node[0]}", is_highlighted)

            left_child_idx = 2 * index + 1
            right_child_idx = 2 * index + 2

            if left_child_idx < len(priority_queue):
                left_x, left_y = x - dx, y + vertical_spacing
                self.canvas.create_line(x, y + node_size, left_x, left_y - node_size)
                draw_tree(left_child_idx, left_x, left_y, dx / 2)

            if right_child_idx < len(priority_queue):
                right_x, right_y = x + dx, y + vertical_spacing
                self.canvas.create_line(x, y + node_size, right_x, right_y - node_size)
                draw_tree(right_child_idx, right_x, right_y, dx / 2)

        root_x = canvas_width // 2
        root_y = vertical_spacing

        initial_dx = canvas_width / 4

        draw_tree(0, root_x, root_y, initial_dx)

    def pop_min_animation(self, priority_queue):
        """
        Starte die Animation, die das Min der Priority Queue entfernt
        :param priority_queue: Priority Queue bei der das min entfernt wird
        :return:
        """

        self.stop_animation()
        self.animation_step = 0
        self.animation_active = True
        self.temp_queue = priority_queue.copy()
        self.current_heapify_index = 0
        self.run_pop_min_step()
    def stop_animation(self):
        """
        Stopped alle laufenden Animationen
        :return:
        """

        self.animation_active = False
        if self.after_id is not None:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def run_pop_min_step(self):
        """
        Schrittweise animation des entfernnen des Minimums
        :return:
        """
        if not self.animation_active:
            return

        if self.animation_step == 0:
            root_node = self.temp_queue[0]
            self.draw_priority_queue(self.temp_queue, highlight_node=root_node[1], highlight_distance=root_node[0])
            self.priority_queue_label.config(text="H.extractMin():")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_pop_min_step)

        elif self.animation_step == 1:
            if len(self.temp_queue) == 1:
                self.temp_queue.pop()
                self.draw_priority_queue(self.temp_queue)
                self.priority_queue_label.config(text="H.extractMin():")
                self.stop_animation()
            else:
                self.temp_queue[0] = ("empty", None)
                self.draw_priority_queue(self.temp_queue)
                self.priority_queue_label.config(text="Lösche Wurzel")
                self.animation_step += 1
                self.after_id = self.canvas.after(1000, self.run_pop_min_step)

        elif self.animation_step == 2:
            self.temp_queue[0] = self.temp_queue[-1]
            self.temp_queue.pop()
            self.draw_priority_queue(self.temp_queue)
            self.priority_queue_label.config(text="Letztes Element wird neue Wurzel")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_pop_min_step)

        elif self.animation_step == 3:
            self.priority_queue_label.config(text="Heapify_down():")
            self.heapify_down_step()

    def heapify_down_step(self):
        """
        Schrittweises Heapify-down, zeichnet in jedem Schritt den Baum neu
        :return:
        """
        if not self.animation_active:
            return

        index = self.current_heapify_index
        n = len(self.temp_queue)

        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < n and self.temp_queue[left] < self.temp_queue[smallest]:
            smallest = left

        if right < n and self.temp_queue[right] < self.temp_queue[smallest]:
            smallest = right

        if smallest != index:
            self.temp_queue[index], self.temp_queue[smallest] = self.temp_queue[smallest], self.temp_queue[index]
            self.draw_priority_queue(
                self.temp_queue,
                highlight_node=self.temp_queue[smallest][1],
                highlight_distance=self.temp_queue[smallest][0]
            )
            self.priority_queue_label.config(text="Heapify_down():")
            self.current_heapify_index = smallest
            self.after_id = self.canvas.after(1000, self.heapify_down_step)
        else:
            self.priority_queue_label.config(text="Heapify_down() abgeschlossen")
            self.draw_priority_queue(
                self.temp_queue
            )
            self.animation_step = 3
            self.stop_animation()

    def insert_animation(self, priority_queue, new_element):
        """
        Startet die Insert animation
        :param priority_queue: priority queue
        :param new_element: element was eingefügt werden solll
        :return:
        """
        self.stop_animation()
        self.animation_step = 0
        self.animation_active = True

        self.temp_queue = priority_queue.copy()
        self.new_element = new_element
        self.run_insert_step()

    def run_insert_step(self):
        """
        Schrittweise animation des Einfügens
        :return:
        """
        if not self.animation_active:
            return

        if self.animation_step == 0:

            self.draw_priority_queue(self.temp_queue)
            self.priority_queue_label.config(text="Vor Einfügen:")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_insert_step)

        elif self.animation_step == 1:

            self.temp_queue.append(self.new_element)
            self.draw_priority_queue(self.temp_queue, highlight_node=self.new_element[1],
                                     highlight_distance=self.new_element[0])
            self.priority_queue_label.config(text="Neues Element wird eingefügt")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_insert_step)

        elif self.animation_step == 2:
            self.priority_queue_label.config(text="Heapify_up():")
            self.current_heapify_index = len(self.temp_queue) - 1
            self.heapify_up_step()

    def heapify_up_step(self):
        """
        Schrittweise visualisierung von Heapify-up
        :return:
        """
        if not self.animation_active:
            return

        index = self.current_heapify_index

        if index == 0:
            self.priority_queue_label.config(text="Heapify_up() abgeschlossen")
            self.draw_priority_queue(
                self.temp_queue
            )
            self.stop_animation()
            return

        parent = (index - 1) // 2

        self.draw_priority_queue(
            self.temp_queue,
            highlight_node=self.temp_queue[index][1],
            highlight_distance=self.temp_queue[index][0]
        )

        if self.temp_queue[index] < self.temp_queue[parent]:

            self.temp_queue[index], self.temp_queue[parent] = self.temp_queue[parent], self.temp_queue[index]


            self.draw_priority_queue(
                self.temp_queue,
                highlight_node=self.temp_queue[parent][1],
                highlight_distance=self.temp_queue[parent][0]
            )

            self.current_heapify_index = parent
            self.after_id = self.canvas.after(1000, self.heapify_up_step)
        else:
            self.priority_queue_label.config(text="Heapify_up() abgeschlossen")
            self.draw_priority_queue(
                self.temp_queue
            )
            self.stop_animation()

    def remove_node_heapify_animation(self, priority_queue, target_node):
        """
        Entfernt spezifischen Knoten aus der Priorityqueue und animiert die Schritte
        :param priority_queue: priority Queue
        :param target_node: zu entfernender Knoten
        :return:
        """
        self.stop_animation()
        self.animation_step = 0
        self.animation_active = True
        self.temp_queue = priority_queue.copy()
        self.target_node = target_node

        if not any(node == self.target_node for _, node in self.temp_queue):
            return

        self.run_remove_node_heapify_step()

    def run_remove_node_heapify_step(self):
        """
        Schrittweise animation der Heapify Schritte
        :return:
        """
        if not self.animation_active:
            return

        if self.animation_step == 0:
            target_distance = next(dist for dist, node in self.temp_queue if node == self.target_node)
            self.draw_priority_queue(
                self.temp_queue,
                highlight_node=self.target_node,
                highlight_distance=target_distance
            )
            self.priority_queue_label.config(text=f"Markiere Zielknoten {self.target_node}")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_remove_node_heapify_step)

        elif self.animation_step == 1:
            for i, (dist, node) in enumerate(self.temp_queue):
                if node == self.target_node:
                    self.temp_queue[i] = ("empty", None)
                    break
            self.draw_priority_queue(self.temp_queue)
            self.priority_queue_label.config(text=f"Knoten {self.target_node} als 'leer' markiert")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_remove_node_heapify_step)

        elif self.animation_step == 2:
            self.draw_priority_queue(self.temp_queue)
            self.priority_queue_label.config(text=f"Heap mit 'leerem' Knoten (vor Entfernung)")
            self.animation_step += 1
            self.after_id = self.canvas.after(1000, self.run_remove_node_heapify_step)

        elif self.animation_step == 3:
            self.temp_queue[:] = [(dist, node) for dist, node in self.temp_queue if node is not None]
            self.draw_priority_queue(self.temp_queue)
            self.priority_queue_label.config(
                text=f"'Leerer' Knoten entfernt. Heap ist ungültig und wird neu aufgebaut...")
            self.animation_step += 1
            self.after_id = self.canvas.after(2000, self.run_remove_node_heapify_step)  # Longer delay here

        elif self.animation_step == 4:
            self.current_heapify_index = len(self.temp_queue) // 2 - 1
            self.priority_queue_label.config(text="Starte Heapify Down...")
            self.after_id = self.canvas.after(1000, self._heapify_step)

    def _heapify_step(self):
        """
        Abschluss schritt bei den Heapify Operationen
        :return:
        """
        if not self.animation_active:
            return

        if self.current_heapify_index < 0:
            self.priority_queue_label.config(text="Heapify abgeschlossen. Heap ist nun gültig.")
            self.draw_priority_queue(self.temp_queue)
            self.stop_animation()
            return

        current_node = self.temp_queue[self.current_heapify_index][1]
        current_distance = self.temp_queue[self.current_heapify_index][0]
        self.draw_priority_queue(
            self.temp_queue,
            highlight_node=current_node,
            highlight_distance=current_distance
        )
        self.priority_queue_label.config(text=f"Heapify Down: Verarbeite Knoten {current_node}")
        self.after_id = self.canvas.after(1000, self._sift_down_step, self.current_heapify_index)

    def _sift_down_step(self, index):
        """
        Heapify down starting von index knoten
        :param index: Knoten index, für Heapify down
        :return:
        """
        if not self.animation_active:
            return

        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.temp_queue) and self.temp_queue[left][0] < self.temp_queue[smallest][0]:
            smallest = left
        if right < len(self.temp_queue) and self.temp_queue[right][0] < self.temp_queue[smallest][0]:
            smallest = right

        if smallest != index:
            self.temp_queue[index], self.temp_queue[smallest] = self.temp_queue[smallest], self.temp_queue[index]
            self.draw_priority_queue(
                self.temp_queue,
                highlight_node=self.temp_queue[smallest][1],
                highlight_distance=self.temp_queue[smallest][0]
            )
            self.after_id = self.canvas.after(1000, self._sift_down_step, smallest)
        else:
            self.current_heapify_index -= 1
            self.after_id = self.canvas.after(1000, self._heapify_step)



    def setup_frames(self):
        """
        Initiales Canvas setup
        :return:
        """
        self.canvas_frame.pack_propagate(False)
        self.canvas_frame.config(width=800, height=400)


