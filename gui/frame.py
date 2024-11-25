import os.path
import random
import tkinter.simpledialog
from tkinter import *
import math
from tkinter import filedialog
import json


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
        self.canvas = Canvas(self, width=1000, height=1000, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, columnspan=6)
        #create buttons

        self.button_frame = Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=6, pady=10)

        self.next_button = Button(self.button_frame, text="Next Step", command=parent.next_step)
        self.next_button.grid(row=1, column=0, padx=5, sticky="w")

        self.prev_button = Button(self.button_frame, text="Previous Step", command=parent.prev_step)
        self.prev_button.grid(row=1, column=1, padx=5, sticky="w")

        self.fast_forward_button = Button(self.button_frame, text="Fast Forward", command=parent.fast_forward)
        self.fast_forward_button.grid(row=1, column=2, padx=5, sticky="w")
        self.fast_forward_button = Button(self.button_frame, text="Pause", command=parent.pause)
        self.fast_forward_button.grid(row=1, column=3, padx=5, sticky="w")

        self.print_currently_loaded_graph_button = Button(self.button_frame, text="print graph to console", command=self.print_loaded_graph)
        self.print_currently_loaded_graph_button.grid(row=1, column=4, padx=5, sticky="w")

        self.button_frame_alg = Frame(self)
        self.button_frame_alg.grid(row=0, column=6, pady=10)

        self.starting_button = Button(self.button_frame_alg, text="select Starting node", command=parent.start_algorithm)
        self.starting_button.grid(row=0, column=0, padx=5, sticky="w")




        #Bind option to canvas

        self.canvas.bind("<Button-1>", self.add_node_or_edge)
        self.canvas.bind("<Button-3>", self.remove_clicked_element)
        self.focus_set()
        self.bind("<Right>", self.go_to_next_step)
        self.bind("<Left>", self.go_step_back)
        self.bind("<Up>", self.go_fast_forward)
        self.bind("<Down>", self.pause_fast_forward)

        # Menü Bar oben
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)

        # Optionen Menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.debug_mode_var = BooleanVar(value=True)
        # Add commands to the "Options" menu
        self.options_menu.add_command(label="Setting", command=self.open_settings)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Quit", command=parent.quit)
        self.options_menu.add_checkbutton(label="Toggle Debug mode", variable=self.debug_mode_var, command=self.toggle_debug_mode)

        # Graph optionen Menu
        self.graph_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Graph", menu=self.graph_menu)
        self.graph_menu.add_command(label="Load Default Graph", command=parent.load_default_graph)
        self.graph_menu.add_command(label="Clear Graph", command=parent.clear_graph)
        self.graph_menu.add_command(label="Import Graph", command=self.import_graph)
        self.graph_menu.add_command(label="Export Graph", command=self.export_graph)

        # Creation menu
        self.creation_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Create", menu=self.creation_menu)

        #display current mode with  checkmark
        self.node_mode_var = BooleanVar(value=False)
        self.edge_mode_var = BooleanVar(value=False)
        self.edge_mode_random_var = BooleanVar(value=True)

        self.creation_menu.add_checkbutton(label="Add Node", variable=self.node_mode_var,
                                           command=self.toggle_node_creation_mode)
        self.creation_menu.add_checkbutton(label="Add Edge", variable=self.edge_mode_var,
                                           command=self.toggle_edge_creation_mode)
        self.creation_menu.add_checkbutton(label="random Edge weight mode", variable=self.edge_mode_random_var,
                                           command=self.toggle_random_edge_weight)

        self.algorithm_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Algorithmen", menu=self.algorithm_menu)
        self.dijk_L = BooleanVar(value=False)
        self.dijk_PQ = BooleanVar(value=True)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Liste", variable=self.dijk_L , command=self.toggle_dijk_L)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Priority Queue", variable=self.dijk_PQ, command=self.toggle_dijk_PQ)


    def toggle_random_edge_weight(self):

        self.random_edge_mode = self.edge_mode_random_var.get()
        print("Random edge weight mode is now", "on" if self.random_edge_mode else "off")



    def add_node_or_edge(self, event):
        if self.parent.node_creation_mode == True:
            if self.parent.debug:
                print("Node_Event triggered by Mouse clicked at", event.x, event.y)
            self.add_node(event)
        if self.parent.edge_creation_mode == True:
            if self.parent.debug:
                print("Edge_Event triggered by Mouse clicked at", event.x, event.y)
            self.add_edge(event)

    def toggle_debug_mode(self):
        self.parent.debug = self.debug_mode_var.get()
        print("Debug mode is now", "on" if self.parent.debug else "off")

    def remove_clicked_element(self, event):
        x, y = event.x, event.y
        print("removal event at:", event.x, event.y)

        node = self.get_node_at_position(x, y)
        if node:
            print("deleting node at: Position noch genau bestimmen, nicht vom event sondern vom knoten")
            self.delete_note(node)


        # später, aktuell keine edge deletion möglich
        '''edge = self.get_edge_at_coordinates(x, y)
        if edge:
            print("deleting edge at: ", x, y)
        #wie eine Kante finden?'''

    def delete_note(self, node):
        if node in self.parent.graph:
            del self.parent.graph[node]

        for nb in self.parent.graph.values():
            if node in nb:
                del nb[node]
        if node in self.parent.node_positions:
            del self.parent.node_positions[node]
        self.parent.selected_nodes = []
        print(f"Knoten {node} gelöscht")
        self.parent.reset()

    #Hier soll ein Settingsmenu geöffnet werden was settings speichert und beim laden der app läd
    def open_settings(self):
        if self.parent.debug:
            print("Opening settings...")

    # hilfsunktion um die parent funktion zu callen für die Keybinds
    def go_to_next_step(self, event):
        print("testkeybind forward")
        self.parent.next_step()
    def go_step_back(self, event):
        print("testkeybind back")
        self.parent.prev_step()

    def go_fast_forward(self, event):
        print("testkeybind auto")
        self.parent.fast_forward_paused = False
        self.parent.fast_forward()
    def pause_fast_forward(self, event):
        print("testkeybind pause")
        self.parent.pause()


    # gibt den aktuellen graphen auf der Konsole aus -> debug optionen
    def print_loaded_graph(self):
        if self.parent.debug:
            print("currently Loaded graph: ")
        print(self.parent.graph)
        print(self.parent.node_positions)
        print(self.parent.steps_finished_algorithm)

    # select dijkstra mit List as algorithm
    def toggle_dijk_L(self):
        if self.parent.debug:
            print("Toggle to Dijk mit Liste...")
        self.parent.selected_algorithm = "Dijkstra_List"
        self.parent.code_frame.set_algorithm("Dijkstra_List")
        self.parent.reset()
        self.dijk_L.set(True)
        self.dijk_PQ.set(False)

    #select dijkstra mit Pq as algorithm
    def toggle_dijk_PQ(self):
        if self.parent.debug:
            print("Toggle to Dijk mit PQ...")
        self.parent.selected_algorithm = "Dijkstra_PQ"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(True)

    #Node Creation mode toggle
    def toggle_node_creation_mode(self):
        if self.parent.debug:
            print("Toggling node creation mode...")
        self.parent.node_creation_mode = True
        self.parent.edge_creation_mode = False
        self.node_mode_var.set(True)
        self.edge_mode_var.set(False)

    #Edge Creation mode
    def toggle_edge_creation_mode(self):
        if self.parent.debug:
            print("Toggling Edge creation mode...")
        self.parent.node_creation_mode = False
        self.parent.edge_creation_mode = True
        self.node_mode_var.set(False)
        self.edge_mode_var.set(True)

    #Knoten hinzufügen
    def add_node(self, event):
        if not self.parent.node_creation_mode:
            return

        x, y = event.x, event.y
        new_node = self.get_next_id()
        self.parent.graph[new_node] = {}
        self.parent.node_positions[new_node] = (x, y)

        print(f"Node {new_node} added at ({x}, {y})")
        self.parent.reset()

    # hilfs funktion damit löschen von knoten nicht der erstellen verhindert, da sonst duplikate erstellt werden, was alles breaked
    def get_next_id(self):
        ex_id = {int (node) for node in self.parent.graph.keys()}
        newid  = 1
        while newid in ex_id:
            newid += 1
        return str(newid)

    #Kante hinzufügen, MAYBE RANDOM EDGE WEIGHT MODE?
    def add_edge(self, event):

        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y) # Ausgeheneder Knoten

        if clicked_node: # falls knoten existiert
            if len(self.parent.selected_nodes) == 2:
                self.parent.selected_nodes = []
                self.parent.reset()

            self.parent.selected_nodes.append(clicked_node) #speicher ihn zwischen
            print(f"Selected node: {clicked_node}")

            # !!!!!!!!!checke das 2. knoten != 1. knoten. und neue kante soll alte überschreiben, keine mehrfachen kann zwischen 2 knoten
            if len(self.parent.selected_nodes) == 2:  #wenn 2 noten im Zwischenspeicher sind ,dann füge Kante hinzu
                node1, node2 = self.parent.selected_nodes

                #dialog öffnen der nach gewicht fragt
                if self.random_edge_mode:
                    print("random mode")
                    weight = random.randint(0, 100)
                else:
                    print("input mode")
                    weight = tkinter.simpledialog.askinteger("Input edge weight", "Input Edge Weight as a Integer")

                if not node1 == node2 and weight is not None:
                    self.parent.graph[node1][node2] = weight#Füge weight hinzu
                    self.parent.selected_nodes.clear()#Resette den Zwischenspeicher
                    print(f"Edge added from {node1} to {node2} with weight {weight}")


            self.parent.update_gui() # Aktualisiere Gui

        self.parent.reset()


    # Hilfsfunktion die einen Knoten returned der in einem Radius von 30px zu click coordinaten ist. Wird benötigt für die Erstellung von Kanten
    def get_node_at_position(self, x, y):

        for node, (nx, ny) in self.parent.node_positions.items():
            if math.hypot(nx - x, ny - y) <= 30:
                return node
        return None

    def get_edge_at_coordinates(self, x, y):
        for node_s, neighbor in self.parent.graph.items():
            for node_e in neighbor:
                print(node_s, node_e)
                '''if node_s in self.parent.node_position.items() and node_e in self.parent.node_positions.items():
                    j, l = self.parent.node_position[node_s]
                    w, z = self.parent.node_position[node_e]'''
                distanz = 0 #self.dis_p_to_l(x, y, j, l , w, z)
                if distanz <= 10:
                    return(node_s,node_e)


    # um die distanz zu berechnen, damit man später edges löschen kann
    def dis_p_to_l(self, x, y, j, l, w, z):
        if(j, l) == (w, z):
            return math.hypot(x - j, y - l)

        num = abs((z -l) * x - (w - j) * y + w * l - z * j)
        den = math.hypot(w - j, z - l)
        return num/den

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

    def import_graph(self):
        print("Todo:importing graph clicked")