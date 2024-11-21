from tkinter import *
import math
class My_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #to Access parent variables
        self.parent = parent

        #put the this frame on screen
        self.pack(pady=20)

        #create buttons
        self.next_button = Button(self, text="Next Step", command=parent.next_step)
        self.next_button.pack(side=LEFT)

        self.prev_button = Button(self, text="Previous Step", command=parent.prev_step)
        self.prev_button.pack(side=LEFT)

        self.fast_forward_button = Button(self, text="Fast Forward", command=parent.fast_forward)
        self.fast_forward_button.pack(side=LEFT)
        self.fast_forward_button = Button(self, text="Pause", command=parent.pause)
        self.fast_forward_button.pack(side=LEFT)

        self.print_currently_loaded_graph_button = Button(self, text="print graph", command=self.print_loaded_graph)
        self.print_currently_loaded_graph_button.pack(side=LEFT)

        #create Canvas
        self.canvas = Canvas(self, width=1000, height=1000, bg="white")
        self.canvas.pack()
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

        self.creation_menu.add_checkbutton(label="Add Node", variable=self.node_mode_var,
                                           command=self.toggle_node_creation_mode)
        self.creation_menu.add_checkbutton(label="Add Edge", variable=self.edge_mode_var,
                                           command=self.toggle_edge_creation_mode)

        self.algorithm_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Algorithmen", menu=self.algorithm_menu)
        self.dijk_L = BooleanVar(value=True)
        self.dijk_PQ = BooleanVar(value=False)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Liste", variable=self.dijk_L , command=self.toggle_dijk_L)
        self.algorithm_menu.add_checkbutton(label="Dijkstra als Priority Queue", variable=self.dijk_PQ, command=self.toggle_dijk_PQ)



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
        print("removal even at:", event.x, event.y)

        node = self.get_node_at_position(x, y)
        if node:
            print("deleting node at: Position noch genau bestimmen, nicht vom event sondern vom knoten")
            # hier dann trigger node delete!

        #wie eine Kante finden?


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

    # select dijkstra mit List as algorithm
    def toggle_dijk_L(self):
        if self.parent.debug:
            print("Toggle to Dijk mit Liste...")
        self.parent.selected_algorithm = True
        self.dijk_L.set(True)  # Check the node mode
        self.dijk_PQ.set(False)  # Uncheck edge mode

    #select dijkstra mit Pq as algorithm
    def toggle_dijk_PQ(self):
        if self.parent.debug:
            print("Toggle to Dijk mit PQ...")
        self.parent.selected_algorithm = False
        self.dijk_L.set(False)  # Check the node mode
        self.dijk_PQ.set(True)  # Uncheck edge mode

    #Node Creation mode
    def toggle_node_creation_mode(self):
        if self.parent.debug:
            print("Toggling node creation mode...")
        self.parent.node_creation_mode = True
        self.parent.edge_creation_mode = False
        self.node_mode_var.set(True)  # Check the node mode
        self.edge_mode_var.set(False)  # Uncheck edge mode

    #Edge Creation mode
    def toggle_edge_creation_mode(self):
        if self.parent.debug:
            print("Toggling Edge creation mode...")
        self.parent.node_creation_mode = False
        self.parent.edge_creation_mode = True
        self.node_mode_var.set(False)  # Uncheck node mode
        self.edge_mode_var.set(True)  # Check the edge mode

    #Knoten hinzufügen
    def add_node(self, event):
        if not self.parent.node_creation_mode:
            return

        x, y = event.x, event.y
        new_node = f"{len(self.parent.graph) + 1}"
        self.parent.graph[new_node] = {}
        self.parent.node_positions[new_node] = (x, y)
        #self.parent.update_gui()

        print(f"Node {new_node} added at ({x}, {y})")
        self.parent.reset()

    #Kante hinzufügen
    def add_edge(self, event):

        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y) # Ausgeheneder Knoten

        if clicked_node: # falls knoten existiert
            self.parent.selected_nodes.append(clicked_node) #speicher ihn zwischen
            print(f"Selected node: {clicked_node}")

            # !!!!!!!!!checke das 2. knoten != 1. knoten. und neue kante soll alte überschreiben, keine mehrfachen kann zwischen 2 knoten
            if len(self.parent.selected_nodes) == 2:  #wenn 2 noten im Zwischenspeicher sind ,dann füge Kante hinzu
                node1, node2 = self.parent.selected_nodes
                weight = 100  # aktuell noch hardcoded auf 1

                if not node1 == node2:
                    self.parent.graph[node1][node2] = weight # Füge weight hinzu
                self.parent.selected_nodes.clear() # Resette den Zwischenspeicher
                print(f"Edge added from {node1} to {node2} with weight {weight}")


                self.parent.update_gui() # Aktualisiere Gui

        self.parent.reset()


    # Hilfsfunktion die einen Knoten returned der in einem Radius von 30px zu click coordinaten ist. Wird benötigt für die Erstellung von Kanten
    def get_node_at_position(self, x, y):

        for node, (nx, ny) in self.parent.node_positions.items():
            if math.hypot(nx - x, ny - y) <= 30:
                return node
        return None


    def export_graph(self):
        print("Todo:exporting graph clicked")

    def import_graph(self):
        print("Todo:importing graph clicked")