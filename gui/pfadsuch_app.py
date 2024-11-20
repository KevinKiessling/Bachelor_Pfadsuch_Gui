from tkinter import *
from gui.frame import *
import math
class PfadsuchApp(Tk):
    def __init__(self):
        super().__init__()

        #debug mode
        self.debug = True


        self.graph = {}
        self.start_node = 'D'
        self.steps = []
        self.current_step = -1
        self.node_creation_mode = False  # Knoten erstellungsmodus
        self.edge_creation_mode = False  #  Knoten erstellungsmodus

        self.node_positions = {}  # speichert Knoten positionen
        self.selected_nodes = []  #Hilfe um Kanten zu erstellen
        self.selected_algorithm = True # True für dijkstra mit Liste, false für Priority queue


        #titel
        self.title("Eine Gui zur Visualisierung von Pfadsuch-Algorithmen")
        self.geometry('1500x1000')

        #create the whole gui frame outside of this class
        self.gui_frame = My_Frame(self)
        self.load_default_graph()
        self.update_gui()

    def next_step(self):
        if self.debug:
            print("next step")

    def prev_step(self):
        if self.debug:
            print("prev step")

    def fast_forward(self):
        if self.debug:
            print("fast forward")

    def pause(self):
        if self.debug:
            print("pausing")

    def load_default_graph(self):
        if self.debug:
            print("Loading default graph")
        self.graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'A': 4, 'C': 5, 'D': 10},
            'C': {'A': 2, 'B': 5, 'D': 3, 'E': 4},
            'D': {'B': 10, 'C': 3, 'E': 11},
            'E': {'C': 4, 'D': 11, 'P': 5},
            'P': {}
        }
        self.node_positions = {'A': (100, 100), 'B': (300, 100), 'C': (300, 300), 'D': (500, 100), 'E': (500, 300),
                               'P': (800, 600)}
        self.start_node = 'D'
        self.reset()

    #resets algorithm, but keeps loaded graph
    def reset(self):
        if self.debug:
            print("resetting without clear")
        self.steps = []
        self.current_step = -1
        self.update_gui()
        #self.dijkstra_algorithm.run_dijkstra()  # Correct call to DijkstraAlgorithm's method


    #clear canvas and resets everything to default
    def clear_graph(self):
        if self.debug:
            print("clearing everything")
        self.graph = {}
        self.steps = []
        self.current_step = -1
        self.node_positions = {}
        self.update_gui()
    def update_gui(self):
       # self.reset()
        self.draw_graph()

    #zeichnet den Graph

    def draw_graph(self):
        print("Drawing Graph")
        self.gui_frame.canvas.delete("all")
        node_radius = 30  # Radius of the node circle
        font_size = 16
        #basic draw node
        for node, (x, y) in self.node_positions.items():

            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")
                self.gui_frame.canvas.create_text(x, y, text=node, fill="black", font=("Arial", font_size))
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
                self.gui_frame.canvas.create_text(x, y, text=node, fill="black", font=("Arial", font_size))


        # basic draw edge
        for node, edges in self.graph.items():
            for neighbor, _ in edges.items():
                if neighbor in self.node_positions:
                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]
                    dx = x2 - x1
                    dy = y2 - y1
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance > 0:  # Vermeidung von Division durch 0
                        x1_adjusted = x1 + dx / distance * node_radius
                        y1_adjusted = y1 + dy / distance * node_radius
                        x2_adjusted = x2 - dx / distance * node_radius
                        y2_adjusted = y2 - dy / distance * node_radius
                    else:
                        x1_adjusted, y1_adjusted, x2_adjusted, y2_adjusted = x1, y1, x2, y2

                    self.gui_frame.canvas.create_line(
                        x1_adjusted, y1_adjusted, x2_adjusted, y2_adjusted,
                        width=3,  # Dicke der Linie
                        arrow="last",  # Pfeil am Ende der Linie
                        arrowshape=(10, 12, 5),  # (Basisbreite, Höhe, Spitze)
                        tags="edge"
                    )
