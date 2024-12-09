import os.path
import random
import tkinter.simpledialog
from tkinter import *
import math
from tkinter import filedialog
import json
from tkinter import messagebox

class My_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #to Access parent variables
        self.parent = parent

        #put the this frame on screen
        self.grid(row=0, column=0)
        self.random_edge_mode = True

        self.grid_columnconfigure(0, weight=1, minsize=150)
        self.grid_columnconfigure(1, weight=1, minsize=150)
        self.grid_columnconfigure(2, weight=1, minsize=150)
        self.grid_columnconfigure(3, weight=1, minsize=150)
        self.grid_columnconfigure(4, weight=1, minsize=150)
        self.grid_columnconfigure(5, weight=1, minsize=150)
        # create Canvas
        self.canvas_frame = Frame(self, bd=2,relief="solid")
        self.canvas_frame.grid(row=0, column=0, padx=10, columnspan=6)

        self.canvas = Canvas(self.canvas_frame, width=1000, height=1000, bg="white")
        self.canvas.grid(row=0, column=0)
        #create buttons

        self.button_frame = Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=6, pady=10)

        self.next_button = Button(self.button_frame, text="Next Step", command=parent.next_step)
        self.next_button.grid(row=1, column=0, padx=5, sticky="w")

        self.prev_button = Button(self.button_frame, text="Previous Step", command=parent.prev_step)
        self.prev_button.grid(row=1, column=1, padx=5, sticky="w")

        self.fast_forward_button = Button(self.button_frame, text="Fast Forward", command=self.go_forward_button)
        self.fast_forward_button.grid(row=1, column=2, padx=5, sticky="w")
        self.fast_forward_button = Button(self.button_frame, text="Pause", command=parent.pause)
        self.fast_forward_button.grid(row=1, column=3, padx=5, sticky="w")

        #self.print_currently_loaded_graph_button = Button(self.button_frame, text="print graph to console", command=self.print_loaded_graph)
        #self.print_currently_loaded_graph_button.grid(row=1, column=4, padx=5, sticky="w")

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
        # Menü Bar oben
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)

        # Optionen Menü
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.debug_mode_var = BooleanVar(value=True)
        self.options_menu.add_command(label="Setting", command=self.open_settings)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Quit", command=parent.quit)
        self.options_menu.add_checkbutton(label="Toggle Debug", variable=self.debug_mode_var, command=self.toggle_debug_mode)
        self.edge_mode_random_var = BooleanVar(value=True)

        self.options_menu.add_checkbutton(label="Random Edge weight", variable=self.edge_mode_random_var,
                                           command=self.toggle_random_edge_weight)

        # Graph optionen Menu
        self.graph_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Graph", menu=self.graph_menu)
        self.graph_menu.add_command(label="Load Default Graph", command=parent.load_default_graph)
        self.graph_menu.add_command(label="Clear Graph", command=parent.clear_graph)
        self.graph_menu.add_command(label="Import Graph", command=self.import_graph)
        self.graph_menu.add_command(label="Export Graph", command=self.export_graph)

        # Algorithmen menü
        self.algorithm_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Algorithmen", menu=self.algorithm_menu)
        self.dijk_L = BooleanVar(value=False)
        self.dijk_PQ = BooleanVar(value=True)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Liste", variable=self.dijk_L , command=self.toggle_dijk_L)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Priority Queue", variable=self.dijk_PQ, command=self.toggle_dijk_PQ)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Edit Kantengewicht", command=self.edit_edge_weight)

        self.help = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Hilfe", menu=self.help)
        self.help.add_command(label="Tutorial", command=self.open_tutorial)


    def open_tutorial(self):
        if self.parent.debug:
            print("Öffne Tutorial, todo")

    def edit_edge_weight(self):

        prompt_window = Toplevel(self)
        prompt_window.title("Kantengewicht ändern")


        Label(prompt_window, text="Start Knoten:").grid(row=0, column=0, padx=10, pady=5)
        start_node_entry = Entry(prompt_window)
        start_node_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(prompt_window, text="End Knoten:").grid(row=1, column=0, padx=10, pady=5)
        end_node_entry = Entry(prompt_window)
        end_node_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(prompt_window, text="Neues Gewicht:").grid(row=2, column=0, padx=10, pady=5)
        weight_entry = Entry(prompt_window)
        weight_entry.grid(row=2, column=1, padx=10, pady=5)


        def confirm_change():
            start_node = start_node_entry.get()
            end_node = end_node_entry.get()
            try:
                new_weight = int(weight_entry.get())
            except ValueError:
                messagebox.showerror("Error, Input nicht valide", "Bitte nicht negativen Integer eingeben")
                return

            if start_node in self.parent.graph and end_node in self.parent.graph[start_node]:

                self.parent.graph[start_node][end_node] = new_weight

                messagebox.showinfo("Erfolg", f"Kantengewicht von {start_node} → {end_node} geändert zu {new_weight}.")
                self.parent.update_gui()
                prompt_window.destroy()
            else:
                messagebox.showerror("Fehler", "Kante nicht gefunden, bitte sicherstellen das die Kante existiert")

        Button(prompt_window, text="Apply", command=confirm_change).grid(row=3, column=0, columnspan=2, pady=10)


        Button(prompt_window, text="Cancel", command=prompt_window.destroy).grid(row=4, column=0, columnspan=2, pady=10)


    #Schalted zwischen manueller kanten gewicht eingabe und Random 0-100 um
    def toggle_random_edge_weight(self):

        self.random_edge_mode = self.edge_mode_random_var.get()
        if self.parent.debug:
            print("Random edge weight mode is now", "on" if self.random_edge_mode else "off")



    #Schaltet debug mode an/aus
    def toggle_debug_mode(self):
        self.parent.debug = self.debug_mode_var.get()
        print("Debug mode is now", "on" if self.parent.debug else "off")

    #Löscht Knoten oder Kante an Klick position,
    def remove_clicked_element(self, event):
        x, y = event.x, event.y
        if self.parent.debug:
            print("removal event at:", event.x, event.y)

        node = self.get_node_at_position(x, y)
        if node:
            if self.parent.debug:
                print("Knoten gelöscht")
            self.delete_note(node)
            return

        kante = self.get_edge_at_coordinates(x, y)
        if kante:

            s, e = kante
            if e in self.parent.graph[s]:
                del self.parent.graph[s][e]
                if self.parent.debug:
                    print(f" Kante {s}, {e} gelöscht")
                self.parent.reset()
                return
            else:
                if self.parent.debug:
                    print("Error, keine Kante gefunden")

    #Löscht übergebenen Knoten
    def delete_note(self, node):
        if node in self.parent.graph:
            del self.parent.graph[node]

        for nb in self.parent.graph.values():
            if node in nb:
                del nb[node]
        if node in self.parent.node_positions:
            del self.parent.node_positions[node]
        self.parent.selected_nodes = []
        if self.parent.debug:
            print(f"Knoten {node} gelöscht")
        self.parent.reset()

    #Hier soll ein Settingsmenu geöffnet werden was settings speichert und beim laden der app läd
    def open_settings(self):
        if self.parent.debug:
            print("Öffne Einstellungen, kommt später")

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
        self.dijk_PQ.set(False)

    #select dijkstra mit Pq as algorithm
    def toggle_dijk_PQ(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstram mit Priority Queue")
        self.parent.selected_algorithm = "Dijkstra_PQ"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(True)



    #Knoten hinzufügen
    def add_node(self, event):

        x, y = event.x, event.y

        clicked_node = self.get_node_at_position(x, y)
        self.parent.reset()
        if clicked_node:
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
        if self.parent.debug:
            print(f"Knoten {new_node} hinzugefügt an Position ({x}, {y})")
        self.parent.reset()

    # hilfs funktion damit löschen von knoten nicht der erstellen verhindert, da sonst duplikate erstellt werden, was alles breaked
    def get_next_id(self):
        ex_id = {int (node) for node in self.parent.graph.keys()}
        newid  = 1
        while newid in ex_id:
            newid += 1
        return str(newid)

    #Kante hinzufügen in 2 schritten, 1. Markieren und speichern des Ausgangsknoten, 2. aufruf speichert den zielknoten und zieht kante
    def add_edge(self, event):

        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node: # falls knoten existiert
            if len(self.parent.selected_nodes) == 2:
                self.parent.selected_nodes = []
                self.parent.reset()

            self.parent.selected_nodes.append(clicked_node)
            if self.parent.debug:
                print(f"Startknoten gewählt : {clicked_node}")


            if len(self.parent.selected_nodes) == 2:
                node1, node2 = self.parent.selected_nodes

                #dialog öffnen der nach gewicht fragt
                if self.random_edge_mode:
                    if self.parent.debug:
                        print("random mode")
                    weight = random.randint(0, 100)
                else:
                    if self.parent.debug:
                        print("input mode")
                    weight = tkinter.simpledialog.askinteger("Kantengewicht Eingeben", "Kantengewicht Eingeben")

                if not node1 == node2 and weight is not None:
                    self.parent.graph[node1][node2] = weight
                    self.parent.selected_nodes.clear()
                    if self.parent.debug:
                        print(f"Kante von {node1} zu {node2} mit Gewicht {weight} hinzugefügt")


            self.parent.update_gui() # Aktualisiere Gui

        self.parent.reset()


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
                self.parent.reset()
            else:
                print("Fehlerhafte Input datei, Graph oder Node_Position nicht gefunden")
        except Exception as e:
            print(f"Importing error : {e}")