import os.path
import random
import string
import tkinter.simpledialog
from tkinter import *
import math
from tkinter import filedialog
import json
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
class My_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.operation_history = []
        self.available_ids = self.generate_node_ids()
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)


        self.canvas_frame = Frame(self, bd=2, relief="solid")
        self.canvas_frame.grid(row=0, column=0, padx=10, columnspan=6, sticky="nsew")

        self.canvas = Canvas(self.canvas_frame, bg="white", width=1000, height=1000)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.button_frame = Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=6, pady=10)



        self.next_button = Button(self.button_frame, text="1 Schritt vor", command=parent.next_step)
        self.next_button.grid(row=1, column=0, padx=5, sticky="w")

        self.prev_button = Button(self.button_frame, text="1 Schritt zurück", command=parent.prev_step)
        self.prev_button.grid(row=1, column=1, padx=5, sticky="w")

        self.fast_forward_button = Button(self.button_frame, text="Vorspulen", command=self.go_forward_button)
        self.fast_forward_button.grid(row=1, column=2, padx=5, sticky="w")
        self.fast_forward_button = Button(self.button_frame, text="Pausieren", command=parent.pause)
        self.fast_forward_button.grid(row=1, column=3, padx=5, sticky="w")
        self.button_frame_alg = Frame(self)
        self.button_frame_alg.grid(row=0, column=6, pady=10)

        self.starting_button = Button(self.button_frame_alg, text="Algorithmus Starten", command=parent.start_algorithm)
        self.starting_button.grid(row=0, column=0, padx=5, sticky="w")

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.add_edge)
        self.canvas.bind("<Button-2>", self.remove_clicked_element)
        self.focus_set()
        self.bind("<Right>", self.go_to_next_step)
        self.bind("<Left>", self.go_step_back)
        self.bind("<Up>", self.go_fast_forward)
        self.bind("<Down>", self.pause_fast_forward)
        self.bind("<Return>", self.start_alg)
        self.bind("<Control-z>", self.undo_last_operation)

        # Menü Bar oben
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)

        # Optionen Menü
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Optionen", menu=self.options_menu)
        self.debug_mode_var = BooleanVar(value=True)
        self.options_menu.add_command(label="Einstellungen", command=self.open_settings)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Beenden", command=parent.quit)

        # Graph optionen Menu
        self.graph_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Graph Funktionen", menu=self.graph_menu)
        self.graph_menu.add_command(label="Lade Default Graph", command=parent.load_default_graph)
        self.graph_menu.add_command(label="Lösche Graph", command=parent.clear_graph)
        self.graph_menu.add_command(label="Importiere Graph", command=self.import_graph)
        self.graph_menu.add_command(label="Exportiere Graph", command=self.export_graph)

        # Algorithmen menü
        self.algorithm_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Algorithmen", menu=self.algorithm_menu)
        self.dijk_L = BooleanVar(value=False)
        self.dijk_PQ_lazy = BooleanVar(value=True)
        self.dijk_PQ = BooleanVar(value=False)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Liste", variable=self.dijk_L , command=self.toggle_dijk_L)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Priority Queue(Lazy Deletion)", variable=self.dijk_PQ_lazy, command=self.toggle_dijk_PQ_lazy)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Priority Queue", variable=self.dijk_PQ,
                                            command=self.toggle_dijk_PQ)

        self.help = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Hilfe", menu=self.help)
        self.help.add_command(label="Tutorial", command=self.open_tutorial)


    def open_tutorial(self):
        if self.parent.debug:
            print("Öffne Tutorial, todo")
        tutorial_window = Toplevel(self)
        tutorial_window.title("Hilfe")
        tutorial_window.geometry("700x600")
        tutorial_window.transient(self.parent)

        tutorial_text = Label(tutorial_window, text="TUTORIAL.\n"
                                                    "Knoten Per Linksklick erstellen.\n"
                                                    "Kanten Per Rechtsklick erstellen.\n"
                                                    "Elemente mit Mittlerer Maustaste Löschen.\n"
                                                    "Linksklick auf existierenden Knoten wählt ihn als Startknoten.\n"
                                                    "per Enter Taste oder Start algorithm Button den algorithmus starten.\n"
                                                    "Falls kein Startknoten gewählt wurde, wird jetzt nach einem gefragt\n"
                                                    "Mit Pfeiltaste links/rechts einen Schritt vor/zurück.\n"
                                                    "Mit Pfeiltaste hoch automatisches durchlaufen.\n"
                                                    "Mit Pfeiltaste unten automatisches durchlaufen pausieren.\n"
                                                    "Einstellungsoptionen für Zufällige Kantengewichte, debug to console und Animationsgeschwindigkeit.\n"
                                                    "und möglichkeit den aktuellen Graphen als Default Graph zu speichern", justify="left")
        tutorial_text.pack(pady=10, padx=10)


        cancel_button = Button(tutorial_window, text="Okay", command=tutorial_window.destroy)
        cancel_button.pack(pady=10)


    def undo_last_operation(self, event=None):
        if self.parent.debug:
            print(self.operation_history)
        if not self.operation_history:
            if self.parent.debug:
                print("Keine Operation im speicher")
            return

        last_operation = self.operation_history.pop()
        op_type, op_data = last_operation
        if op_type == "add_node":
            self.delete_note(op_data)
        elif op_type == "add_edge":
            node1, node2, _ = op_data
            if node2 in self.parent.graph[node1]:
                del self.parent.graph[node1][node2]
                if self.parent.debug:
                    print(f"Strg+z Kante von {node1} nach {node2} rückgängig gemacht")
        self.parent.reset()
        if self.parent.debug:
            print(self.operation_history)

    #Löscht Knoten oder Kante an Klick position,
    def remove_clicked_element(self, event):
        x, y = event.x, event.y
        if self.parent.debug:
            print("removal event at:", event.x, event.y)

        node = self.get_node_at_position(x, y)
        if node:
            if self.parent.debug:
                print("Knoten gelöscht")
            self._remove_from_history("add_node", node)
            self.delete_note(node)
            return

        kante = self.get_edge_at_coordinates(x, y)
        if kante:

            s, e = kante
            if e in self.parent.graph[s]:
                del self.parent.graph[s][e]
                if self.parent.debug:
                    print(f" Kante {s}, {e} gelöscht")
                self._remove_from_history("add_edge", (s, e))
                self.parent.reset()
                return
            else:
                if self.parent.debug:
                    print("Error, keine Kante gefunden")

    def _remove_from_history(self, op_type, item):
        if self.parent.debug:
            print(op_type)
            print(item)
        for i in range(len(self.operation_history)):
            operation = self.operation_history[i]
            if operation[0] == op_type:
                if op_type == "add_node" and operation[1] == item:
                    del self.operation_history[i]
                    break
                elif op_type == "add_edge" and (operation[1][0] == item[0] and operation[1][1] == item[1]):
                    print("yo")
                    del self.operation_history[i]
                    break
    #Löscht übergebenen Knoten
    def delete_note(self, node):
        if node in self.parent.graph:
            del self.parent.graph[node]
            self.available_ids.insert(0, node)

        for nb in self.parent.graph.values():
            if node in nb:
                del nb[node]
        if node in self.parent.node_positions:
            del self.parent.node_positions[node]
        self.parent.selected_nodes = []
        if self.parent.debug:
            print(f"Knoten {node} gelöscht")
        self.parent.reset()

    #Öffnet Einstellungsmenu, welches den Debug mode, random mode und Animationspeed einstellen lässt und in der Config.json speichert.
    def open_settings(self):
        settings_window = Toplevel(self)
        settings_window.title("Einstellungen")
        settings_window.geometry("500x400")
        settings_window.transient(self.parent)

        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=BOTH, expand=True)

        general_tab = Frame(notebook)
        notebook.add(general_tab, text="Allgemeine Einstellungen")

        debug_var = BooleanVar(value=self.parent.debug)
        debug_checkbox = Checkbutton(
            general_tab,
            text="Debug Mode",
            variable=debug_var
        )
        debug_checkbox.pack(anchor="w", pady=10, padx=10)

        random_mode_var = BooleanVar(value=self.parent.random_edge_mode)
        random_random_checkbox_frame = Frame(general_tab)
        random_random_checkbox_frame.pack(anchor="w", pady=10, padx=10)
        random_checkbox = Checkbutton(
            random_random_checkbox_frame,
            text="Zufälliges Kantengewicht",
            variable=random_mode_var
        )
        random_checkbox.grid(row=0,column=0)

        max_weight_var = IntVar(value=self.parent.max_edge_weight)
        def validate_input(new_val):
            if new_val == "" or new_val.isdigit():
                return True
            else:
                return False

        validate_command = settings_window.register(validate_input)

        max_weight_entry_field = Entry(random_random_checkbox_frame, textvariable=max_weight_var, width=10, validate="key", validatecommand=(validate_command, "%P"))
        max_weight_entry_field.grid(row=0, column=1)
        max_weight_label = Label(random_random_checkbox_frame, text="Maximales Gewicht")
        max_weight_label.grid(row=0, column=2)



        save_cur_a_d_var = BooleanVar(value=False)
        save_cur_a_d_cb = Checkbutton(
            general_tab,
            text="Aktuellen Graphen als Default Speichern",
            variable=save_cur_a_d_var
        )
        save_cur_a_d_cb.pack(anchor="w", pady=10, padx=10)


        Label(general_tab, text="Animationsgeschwindigkeit (ms):").pack(pady=10)
        speed_var = IntVar(value=self.parent.animation_speed)
        speed_slider = ttk.Scale(
            general_tab,
            from_=100,
            to=1000,
            orient=HORIZONTAL,
            length=300,
            variable=speed_var
        )
        speed_slider.pack(pady=10)
        speed_label = Label(general_tab,
                            text=f"Aktuelle Verzögerung bei fast forward Wiedergabe: {speed_var.get()} ms")
        speed_label.pack()

        def update_speed_label(*args):
            speed_label.config(text=f"Verzögerung bei fast forward Wiedergabe: {speed_var.get()} ms")

        speed_var.trace_add("write", update_speed_label)


        def apply_settings():
            self.parent.debug = debug_var.get()
            self.parent.random_edge_mode = random_mode_var.get()
            self.parent.animation_speed = speed_var.get()

            self.parent.max_edge_weight = max_weight_var.get()

            if save_cur_a_d_var.get():
                self.parent.default_graph_pos = self.parent.node_positions
                self.parent.default_graph = self.parent.graph
            self.parent.save_config()
            settings_window.destroy()


        # COLOR TAB
        default_colors = {
            "visited_edge": "#000000",
            "highlighted_edge": "#FF0000",
            "visited_node": "#00FF00",
            "current_node": "#0000FF"
        }
        color_tab = Frame(notebook)
        notebook.add(color_tab, text="Farb Einstellungen")
        def choose_color(element):
            color = colorchooser.askcolor()[1]
            if color:
                if element == 'visited_edge':
                    self.parent.visited_edge_color = color
                    visited_edge_button.config(bg=color)
                elif element == 'highlighted_edge':
                    self.parent.highlighted_edge_color = color
                    highlighted_edge_button.config(bg=color)
                elif element == 'visited_node':
                    self.parent.visited_node_color = color
                    visited_node_button.config(bg=color)
                elif element == 'current_node':
                    self.parent.current_node_color = color
                    current_node_button.config(bg=color)

        def reset_colors():
            # Reset colors to default values
            self.parent.visited_edge_color = default_colors["visited_edge"]
            self.parent.highlighted_edge_color = default_colors["highlighted_edge"]
            self.parent.visited_node_color = default_colors["visited_node"]
            self.parent.current_node_color = default_colors["current_node"]

            # Update button backgrounds to match defaults
            visited_edge_button.config(bg=self.parent.visited_edge_color)
            highlighted_edge_button.config(bg=self.parent.highlighted_edge_color)
            visited_node_button.config(bg=self.parent.visited_node_color)
            current_node_button.config(bg=self.parent.current_node_color)
        def create_color_button(frame, text, element):
            button = Button(frame, text="    ", width=5, command=lambda: choose_color(element))
            button.grid(row=0, column=0, padx=10)
            label = Label(frame, text=text)
            label.grid(row=0, column=1, padx=10)
            return button

        visited_edge_button_frame = Frame(color_tab)
        visited_edge_button = create_color_button(visited_edge_button_frame, "Visited Edge", 'visited_edge')
        visited_edge_button_frame.pack(pady=5)

        highlighted_edge_button_frame = Frame(color_tab)
        highlighted_edge_button = create_color_button(highlighted_edge_button_frame, "Highlighted Edge",
                                                      'highlighted_edge')
        highlighted_edge_button_frame.pack(pady=5)

        visited_node_button_frame = Frame(color_tab)
        visited_node_button = create_color_button(visited_node_button_frame, "Visited Node", 'visited_node')
        visited_node_button_frame.pack(pady=5)

        current_node_button_frame = Frame(color_tab)
        current_node_button = create_color_button(current_node_button_frame, "Current Node", 'current_node')
        current_node_button_frame.pack(pady=5)

        reset_button = Button(color_tab, text="Reset Colors", command=reset_colors)
        reset_button.pack(pady=20)

        button_frame = Frame(settings_window)
        button_frame.pack(pady=20)

        apply_button = Button(button_frame, text="Anwenden", command=apply_settings)
        apply_button.grid(row=0, column=0, padx=10)

        cancel_button = Button(button_frame, text="Abbrechen", command=settings_window.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    # hilfsunktion um die parent funktion zu callen für die Keybinds
    def start_alg (self, event):
        if self.parent.debug:
            print("Beginne Algorithmus")
        self.parent.start_algorithm()
    def go_to_next_step(self, event):
        if self.parent.debug:
            print("1 Schritt vor")
        self.parent.next_step()
    def go_step_back(self, event):
        if self.parent.debug:
            print("1 Schritt zurück")
        self.parent.prev_step()

    def go_forward_button(self):
        if self.parent.debug:
            print("Vorspulen aktiviert")
        self.parent.fast_forward_paused = False
        self.parent.fast_forward()
    def go_fast_forward(self, event):
        if self.parent.debug:
            print("Vorspulen aktiviert")
        self.parent.fast_forward_paused = False
        self.parent.fast_forward()
    def pause_fast_forward(self, event):
        if self.parent.debug:
            print("Vorspulen pausiert")
        self.parent.pause()


    # gibt den aktuellen graphen auf der Konsole aus -> debug optionen
    def print_loaded_graph(self):
        if self.parent.debug:
            print("Aktuell geladener Graph: ")
        print(self.parent.graph)
        print(self.parent.node_positions)
        print(self.parent.steps_finished_algorithm)

    # select dijkstra mit List as algorithm
    def toggle_dijk_L(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstram mit Liste")
        self.parent.selected_algorithm = "Dijkstra_List"
        self.parent.code_frame.set_algorithm("Dijkstra_List")
        self.parent.reset()
        self.dijk_L.set(True)
        self.dijk_PQ_lazy.set(False)
        self.dijk_PQ.set(False)

    #select dijkstra mit Pq as algorithm
    def toggle_dijk_PQ_lazy(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstra mit Priority Queue (Lazy Deletion)")
        self.parent.selected_algorithm = "Dijkstra_PQ_lazy"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ_lazy")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(False)
        self.dijk_PQ_lazy.set(True)
    def toggle_dijk_PQ(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstra mit Priority Queue")
        self.parent.selected_algorithm = "Dijkstra_PQ"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(True)
        self.dijk_PQ_lazy.set(False)



    #Knoten hinzufügen
    def add_node(self, event):

        x, y = event.x, event.y

        clicked_node = self.get_node_at_position(x, y)
        self.parent.reset()
        if clicked_node:
            if self.parent.debug:
                print("Startknoten wählen statt neuer Knoten")
            self.parent.set_starting_node(clicked_node)
            return
        min_dis = 60
        for node, (c_x, c_y) in self.parent.node_positions.items():
            if math.hypot(c_x - x, c_y - y) < min_dis:
                if self.parent.debug:
                    print(f"Knoten ist zu nah an {node}, bitte etwas weiter entfernt einfügen")
                return
        new_node = self.get_next_id()
        self.parent.graph[new_node] = {}
        self.parent.node_positions[new_node] = (x, y)

        self.operation_history.append(("add_node", new_node))
        if self.parent.debug:
            print(f"Knoten {new_node} hinzugefügt an Position ({x}, {y})")

        self.parent.selected_nodes = []
        self.parent.reset()

    # hilfs funktion damit löschen von knoten nicht der erstellen verhindert, da sonst duplikate erstellt werden, was alles breaked
    def get_next_id(self):
        if not self.available_ids:
            raise ValueError("Keine verfügbaren Knoten-IDs mehr.")
        return self.available_ids.pop(0)

    #Kante hinzufügen in 2 schritten, 1. Markieren und speichern des Ausgangsknoten, 2. aufruf speichert den zielknoten und zieht kante
    def add_edge(self, event):

        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node:# falls knoten existiert
            if len(self.parent.selected_nodes) == 2:
                self.parent.selected_nodes = []
                self.parent.reset()

            self.parent.selected_nodes.append(clicked_node)
            if self.parent.debug:
                print(f"Startknoten gewählt : {clicked_node}")


            if len(self.parent.selected_nodes) == 2:
                node1, node2 = self.parent.selected_nodes

                #dialog öffnen der nach gewicht fragt
                if self.parent.random_edge_mode:
                    if self.parent.debug:
                        print("random mode")
                    weight = random.randint(0, self.parent.max_edge_weight)
                else:
                    if self.parent.debug:
                        print("input mode")
                    weight = tkinter.simpledialog.askinteger("Kantengewicht Eingeben", "Kantengewicht Eingeben")
                if weight is None:
                    self.parent.selected_nodes.clear()
                if not node1 == node2 and weight is not None:
                    self.parent.graph[node1][node2] = weight
                    self.operation_history.append(("add_edge", (node1, node2, weight)))
                    self.parent.selected_nodes.clear()
                    if self.parent.debug:
                        print(f"Kante von {node1} zu {node2} mit Gewicht {weight} hinzugefügt")

            self.parent.update_gui() # Aktualisiere Gui
            self.parent.reset()
            return
        clicked_edge = self.get_edge_at_coordinates(x, y)
        if clicked_edge:
            start, end = clicked_edge
            if self.parent.debug:
                print("clicked edge")
            current_weight = self.parent.graph[start][end]
            new_weight = tkinter.simpledialog.askinteger(
                "Kantengewicht ändern",
                f"Aktuelles Gewicht: {current_weight}\nNeues Gewicht eingeben:",
                initialvalue=current_weight
            )
            if new_weight is not None:
                if self.parent.debug:
                    print(f"updating edge weight from {start} -> {end} to {new_weight} ")
                self.parent.graph[start][end] = new_weight
                self.parent.update_gui()
                self.parent.reset()
            return


    # Hilfsfunktion die einen Knoten returned der in einem Radius von 30px zu click coordinaten ist. Wird benötigt für die Erstellung von Kanten
    def get_node_at_position(self, x, y):

        for node, (nx, ny) in self.parent.node_positions.items():
            if math.hypot(nx - x, ny - y) <= 30:
                return node
        return None

    # hilfsfunktion die naheste kante zu 2 koordinaten findet, wird benötigt um Kanten zu löschen
    def get_edge_at_coordinates(self, x, y):
        nearest_edge = None
        min = float('inf')

        for node_s, neighbor in self.parent.graph.items():
            for node_e in neighbor:

                if node_s in self.parent.node_positions and node_e in self.parent.node_positions:
                    x1, y1 = self.parent.node_positions[node_s]
                    x2, y2 = self.parent.node_positions[node_e]
                    dis = self.distance_to_edge(x, y, x1, y1, x2, y2)

                    if dis < min and dis <=5:
                        min = dis
                        nearest_edge = (node_s, node_e)
        return nearest_edge

    # Berechnet die distanz von einem punkt zu einer Linie

    def distance_to_edge(self, x, y, x2, y2, x3, y3):
        if (x2, y2) == (x3, y3):
            return math.hypot(x - x2, y - y2)
        dx, dy = x3 - x2, y3 - y2
        t = ((x - x2) * dx + (y - y2) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        closest_x = x2 + t * dx
        closest_y = y2 + t * dy
        return math.hypot(x - closest_x, y - closest_y)

    # export funktion, Hier wird der Graph als .json file gespeichert. Default directory ist dafür der save_files ordner
    def export_graph(self):
        default_dir = os.path.join(os.getcwd(), "save_files")
        os.makedirs(default_dir, exist_ok=True)
        filepath = filedialog.asksaveasfilename(
            initialdir=default_dir,
            initialfile="Exported_Graph.json",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        try:
            data = {
                "graph": self.parent.graph,
                "node_position": self.parent.node_positions
            }
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"exported to {filepath}")
        except Exception as e:
            print(f"Error:{e}")

    # import funktion, um einen Graphen als .json zu importieren
    def import_graph(self):
        default_dir = os.path.join(os.getcwd(), "save_files")
        os.makedirs(default_dir, exist_ok=True)
        filepath = filedialog.askopenfilename(
            title="Graph .json file zum Importieren auswählen",
            initialdir=default_dir,
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
            if "graph" in data and "node_position" in data:
                self.parent.graph = data["graph"]
                self.parent.node_positions = {node: tuple(pos) for node, pos in data["node_position"].items()}
                if self.parent.debug:
                    print(f" Graph von {filepath} wurde erfolgreich importiert")
                self.update_avai_ids()
                self.operation_history = []
                self.parent.reset()
            else:
                print("Fehlerhafte Input datei, Graph oder Node_Position nicht gefunden")
        except Exception as e:
            print(f"Importing error : {e}")

    def generate_node_ids(self):
        id = list(string.ascii_uppercase)
        pref = ""
        while len(id) < 100:
            for char in string.ascii_uppercase:
                id.append(pref + char)
            pref = id[len(id) - 26]
        return id

    def reset_node_ids(self):
        self.available_ids = self.generate_node_ids()
    def update_avai_ids(self):
        imported_nodes = self.parent.node_positions.keys()
        self.available_ids = [node_id for node_id in self.available_ids if node_id not in imported_nodes]