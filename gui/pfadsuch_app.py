from tkinter import *
from gui.frame import *

class PfadsuchApp(Tk):
    def __init__(self):
        super().__init__()

        #statusvariable
        self.status = True
        #debug mode
        self.debug = True


        self.graph = {}
        self.start_node = 'D'
        self.steps = []
        self.current_step = -1
        self.node_creation_mode = False
        self.edge_creation_mode = False  # New mode for edge creation

        self.node_positions = {}  # Store dynamic node positions
        self.selected_nodes = []  # Store selected nodes for edge creation



        #titel
        self.title("Eine Gui zur Visualisierung von Pfadsuch-Algorithmen")
        self.geometry('1500x1000')

        #create the whole gui frame outside
        My_frame(self)
        self.load_default_graph()

    def next_step(self):
        if self.debug:
            print("next step")

    def prev_step(self):
        if self.debug:
            print("prev step")

    def fast_forward(self):
        if self.debug:
            print("fast forward")

    def load_default_graph(self):
        if self.debug:
            print("Loading default graph")
        self.graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'A': 4, 'C': 5, 'D': 10},
            'C': {'A': 2, 'B': 5, 'D': 3, 'E': 4},
            'D': {'B': 10, 'C': 3, 'E': 11},
            'E': {'C': 4, 'D': 11, 'P': 5},
            'P': {'E': 5}
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

        #self.dijkstra_algorithm.run_dijkstra()  # Correct call to DijkstraAlgorithm's method
        #self.update_gui()

    #clear canvas and resets everything to default
    def clear_graph(self):
        if self.debug:
            print("clearing everything")
        self.graph = {}
        self.steps = []
        self.current_step = -1
        self.node_positions = {}
        #self.update_gui()