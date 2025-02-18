import json
from tkinter import *
from tkinter import messagebox
from gui.Canvas_Frame import *
from gui.Pseudocode_Frame import *
from algorithms.dijkstra_list import *
from algorithms.dijkstra_Priority_queue_lazy import *
from algorithms.dijkstra_Priority_queue import *
from graph_visualizer.graph_visualizer_dijkstra_lazy import *
from graph_visualizer.graph_visualizer_dijkstra import *
from graph_visualizer.graph_visualizer_dijkstra_list import *
from graph_visualizer.graph_visualizer_path import *
import networkx as nx
import math
import copy
class PfadsuchApp(Tk):
    CONFIG_FILE = "config.json"
    def __init__(self):
        super().__init__()
        self.random_edge_mode = False
        self.animation_speed = 100
        self.debug = False
        self.darkmode = False
        self.steps_finished_algorithm = []
        self.shortest_paths = {}
        self.graph = {}
        self.start_node = ''
        self.default_graph_pos = {}
        self.default_graph = {}
        self.current_step = -1
        self.max_edge_weight = 100
        self.font_size = 18
        self.node_rad = 30
        self.font_size_edge_weight = 14
        self.font_size_node_label = 14

        self.fast_forward_paused = False
        self.node_positions = {}
        self.selected_nodes = []
        self.selected_algorithm = "Dijkstra_PQ_lazy"

        #farben für highlighting im pseudocode und in Graph
        self.color_heap = "#d2cd6f"
        self.color_d_v = "violet"
        self.color_discovered_true = "orange"
        self.color_discovered_false = "#00ff40"
        self.color_default = "yellow"
        self.color_edge_highlight = "#4ecdf8"
        self.color_shortest_path = "light blue"

        self.title("Eine Gui zur Visualisierung von Pfadsuch-Algorithmen")
        self.geometry('1850x1100')
        self.minsize(800, 600)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.bind_all("<FocusIn>", self.global_focus_control)

        self.code_frame = Pseudocode_Frame(self)
        self.gui_frame = Canvas_Frame(self)

        self.load_config()
        self.load_default_graph()
        self.code_frame.update_font_size()
        self.code_frame.set_step("Warte auf starten eines Algorithmus")

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.node_rad_original = self.node_rad
        self.font_size_edge_weight_original = self.font_size_edge_weight
        self.font_size_node_label_original = self.font_size_node_label

    def global_focus_control(self, event):
        if event.widget in self.code_frame.winfo_children():
            self.gui_frame.focus_set()

    def on_close(self):
        if self.gui_frame.shortest_paths_window and self.gui_frame.shortest_paths_window.winfo_exists():
            self.gui_frame.shortest_paths_window.destroy()
        self.destroy()

    # Läd config datei beim Start
    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    config = json.load(f)


                #self.debug = config.get("debug", self.debug)
                self.random_edge_mode = config.get("random_edge_mode", self.random_edge_mode)
                self.animation_speed = config.get("animation_speed", self.animation_speed)
                self.default_graph = config.get("default_graph", self.default_graph)
                self.default_graph_pos = config.get("default_graph_pos", self.default_graph_pos)
                self.max_edge_weight = config.get("max_edge_weight", self.max_edge_weight)

                self.color_heap = config.get("color_heap", self.color_heap)
                self.color_d_v = config.get("color_d_v", self.color_d_v)
                self.color_discovered_true = config.get("color_discovered_true", self.color_discovered_true)
                self.color_discovered_false = config.get("color_discovered_false", self.color_discovered_false)
                self.color_edge_highlight = config.get("color_edge_highlight", self.color_edge_highlight)
                self.color_shortest_path = config.get("color_shortest_path", self.color_shortest_path)
                self.font_size = config.get("font_size", self.font_size)


            except json.JSONDecodeError as e:
                if self.debug:
                    print(f"Error loading JSON from {self.CONFIG_FILE}: {e}")
                    print("Using default configuration.")

                self.save_config()

            except Exception as e:
                if self.debug:
                    print(f"An unexpected error occurred while loading the config: {e}")
                    print("Using default configuration.")
                # Optionally reset the config file by saving defaults
                self.save_config()

        else:
            # Config file doesn't exist, save defaults
            self.save_config()


    #speichert config datei als json
    def save_config(self):
        config = {
            #"debug": self.debug,
            "random_edge_mode": self.random_edge_mode,
            "animation_speed": self.animation_speed,
            "default_graph_pos": self.default_graph_pos,
            "default_graph": self.default_graph,
            "max_edge_weight": self.max_edge_weight,
            "color_heap": self.color_heap,
            "color_d_v": self.color_d_v,
            "color_discovered_true": self.color_discovered_true,
            "color_discovered_false": self.color_discovered_false,
            "color_edge_highlight": self.color_edge_highlight,
            "color_shortest_path": self.color_shortest_path
        }
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        #self.update_gui()
        self.code_frame.update_font_size()
    def start_algorithm(self):
        if self.current_step:
            self.steps_finished_algorithm = []
            self.shortest_paths = {}
            self.code_frame.clear_highlights_and_Canvas()
            self.current_step = -1
            self.code_frame.clear_table()

        if self.start_node is None or self.start_node == '':
            start_node = tkinter.simpledialog.askstring("Startknoten wählen", "Bitte Startknoten auswählen")
            self.selected_nodes = []
            if start_node is None:
                return
            start_node_upper = start_node.upper()
            if start_node_upper not in self.graph:
                messagebox.showerror("Knotenfehler", "Startknoten existiert nicht innerhalb des Graphs.")
                return
            self.start_node = start_node_upper


        if self.selected_algorithm == "Dijkstra_PQ_lazy":
            self.dijkstra_pq_lazy = Dijkstra_Priority_Queue_Lazy()
            self.update_gui()
            self.steps_finished_algorithm, self.shortest_paths = self.dijkstra_pq_lazy.run_dijkstra_priority_queue_lazy(self.graph, self.start_node)
            self.code_frame.highlight_step("Starting Algorithm")
            self.code_frame.set_step(f"Starte Dijkstra mit Priority Queue(mit Lazy Deletion)")
        if self.selected_algorithm == "Dijkstra_PQ":
            self.dijkstra_pq = Dijkstra_Priority_Queue()
            self.update_gui()
            self.steps_finished_algorithm, self.shortest_paths = self.dijkstra_pq.run_dijkstra_priority_queue(self.graph, self.start_node)
            self.code_frame.highlight_step("Starting Algorithm")
            self.code_frame.set_step(f"Starte Dijkstra mit Priority Queue(ohne Lazy Deletion)")
        if self.selected_algorithm == "Dijkstra_List":
            self.dijkstra_list = Dijkstra_List()
            self.update_gui()
            self.steps_finished_algorithm, self.shortest_paths = self.dijkstra_list.run_dijkstra_list(
                self.graph, self.start_node)
            self.code_frame.highlight_step("Starting Algorithm")
            self.code_frame.set_step(f"Starte Dijkstra mit Liste")
        self.gui_frame.disable_canvas_interactions()
        self.gui_frame.shortest_paths_button.config(state=DISABLED)
        self.gui_frame.prev_button.config(state=DISABLED)
        self.test_dijkstra_algorithm(self.start_node)


    def set_starting_node(self, node):
        self.start_node = node
        self.selected_nodes = []
        if self.debug:
            print(f" Knoten {node} als Startknoten gesetzt")
        self.selected_nodes = []
        self.steps_finished_algorithm = []
        self.current_step = -1
        self.update_gui()
        self.code_frame.clear_highlights_and_Canvas()
        self.code_frame.clear_table()
        self.code_frame.priority_queue = {}

    def next_step(self):

        if self.debug:
            print("next step")
        if self.steps_finished_algorithm == []:

            self.start_algorithm()

        if self.current_step < len(self.steps_finished_algorithm) -1:
            self.current_step += 1
            self.update_gui()


    def prev_step(self):
        if self.debug:
            print("prev step")
        if self.steps_finished_algorithm == []:
            print("no algorithm loaded")
        if self.current_step > -1:
            self.current_step -= 1
            self.update_gui()
            if self.current_step == -1:
                self.code_frame.update_priority_queue([])


    def fast_forward(self):
        if self.debug:
            print("fast forward")
        if self.fast_forward_paused:
            return
        if self.steps_finished_algorithm == []:
            self.start_algorithm()
        if self.current_step < len(self.steps_finished_algorithm) -1:
            self.current_step += 1
            self.update_gui()
            self.after(self.animation_speed, self.fast_forward)
        else:

            if self.debug:
                print("finished algorithm")


    def pause(self):

        if self.steps_finished_algorithm == []:
            if self.debug:
                print("no algorithm loaded")
            return
        self.fast_forward_paused = True
        if not self.fast_forward_paused:
            self.gui_frame.pause_button.config(state=NORMAL)
        else:
            self.gui_frame.pause_button.config(state=DISABLED)
        if self.debug:
            print("fast forward stopped bei schritt : ", self.current_step)



    # Läd default graph beim starten der App und auf wunsch
    def load_default_graph(self):
        if self.default_graph:
            self.graph = copy.deepcopy(self.default_graph)
            self.node_positions = copy.deepcopy(self.default_graph_pos)
        else:
            self.graph = {
                "1": {"5": 1, "2": 2, "11": 5, "9": 5},
                "2": {"3": 6},
                "3": {"13": 2},
                "4": {"3": 2},
                "5": {"7": 10, "4": 1},
                "6": {"4": 9},
                "7": {"6": 4, "8": 16},
                "8": {"10": 4},
                "9": {"8": 12, "7": 4},
                "10": {},
                "11": {"12": 4, "13": 12},
                "12": {"10": 42},
                "13": {}
            }
            self.node_positions = {
                "1": [412, 433],
                "2": [549, 278],
                "3": [786, 222],
                "4": [455, 96],
                "5": [291, 248],
                "6": [73, 102],
                "7": [48, 488],
                "8": [112, 815],
                "9": [426, 678],
                "10": [657, 949],
                "11": [756, 453],
                "12": [831, 723],
                "13": [956, 364]
            }

        self.selected_nodes = []
        self.scale_loaded_graph()
        self.gui_frame.update_avai_ids()
        self.gui_frame.operation_history = []
        self.reset()

    def scale_loaded_graph(self):

        scale_x = self.gui_frame.canvas_width / 1000
        scale_y = self.gui_frame.canvas_height / 1000

        for node, (x, y) in self.node_positions.items():
            new_x = x * scale_x
            new_y = y * scale_y
            self.node_positions[node] = (new_x, new_y)

    def reset_node_size(self):
        scale_x = self.gui_frame.canvas_width / 1000
        scale_y = self.gui_frame.canvas_height / 1000
        average_scale = (scale_x + scale_y) / 2
        new_radius = self.node_rad * average_scale
        self.node_rad = new_radius
        self.font_size_edge_weight = int(self.font_size_edge_weight_original * average_scale)
        self.font_size_node_label = int(self.font_size_node_label_original * average_scale)

    #Setzt den Algorithmus komplett zurück, aber behält den Graph geladen
    def reset(self):
        self.selected_nodes = []
        self.fast_forward_paused = True
        if self.debug:
            print("resetting without clear")
        self.steps_finished_algorithm = []
        self.current_step = -1
        self.start_node = ""
        self.code_frame.priority_queue = {}
        self.update_gui()
        self.code_frame.clear_highlights_and_Canvas()
        self.gui_frame.canvas.bind("<ButtonPress-1>", self.gui_frame.on_press)
        self.code_frame.clear_table()
        self.gui_frame.close_shortest_path_window()

        self.code_frame.canvas.delete("all")
        self.gui_frame.enable_canvas_interactions()


        self.code_frame.set_step("Warte auf starten eines Algorithmus")
        self.shortest_paths = {}
        if not self.shortest_paths:
            self.gui_frame.shortest_paths_button.config(state=DISABLED)
            self.gui_frame.prev_button.config(state=DISABLED)
        if self.selected_algorithm in {"Dijkstra_PQ_lazy", "Dijkstra_PQ"}:
            self.code_frame.priority_queue_label.config(text="Heap")

        elif self.selected_algorithm == "Dijkstra_List":
            self.code_frame.priority_queue_label.config(text="Liste")




    #Setzt alles zurück und löscht auch den geladenen Graph
    def clear_graph(self):
        if self.debug:
            print("clearing everything")
        self.gui_frame.canvas.bind("<ButtonPress-1>", self.gui_frame.on_press)
        self.graph = {}
        self.steps_finished_algorithm = []
        self.current_step = -1
        self.node_positions = {}
        self.selected_nodes = []
        self.start_node = ""
        self.code_frame.clear_table()
        self.code_frame.clear_highlights_and_Canvas()
        self.gui_frame.operation_history = []
        self.gui_frame.reset_node_ids()
        self.code_frame.priority_queue = {}
        self.update_gui()

    # Updated die Gui
    def update_gui(self):

        if not self.fast_forward_paused:
            self.gui_frame.pause_button.config(state=NORMAL)
        else:
            self.gui_frame.pause_button.config(state=DISABLED)
        self.graph_draw_lazy = Graph_Visualizer_Dijkstra_lazy(self.gui_frame, self.node_positions, self.graph,  self.start_node, self)
        self.graph_draw_normal = Graph_Visualizer_Dijkstra(self.gui_frame, self.node_positions, self.graph,  self.start_node, self)
        self.graph_draw_list = Graph_Visualizer_Dijkstra_List(self.gui_frame, self.node_positions, self.graph, self.start_node, self)
        self.gui_frame.canvas.delete("all")
        self.gui_frame.prev_button.config(state=DISABLED)
        self.gui_frame.cancel_button.config(state=DISABLED)
        self.gui_frame.shortest_paths_button.config(state=DISABLED)
        if self.current_step == -1:
            self.code_frame.set_step("Warte auf Starten eines Algorithmus")
            if self.selected_algorithm == "Dijkstra_PQ_lazy":
                self.graph_draw_lazy.draw_graph_dijkstra_lazy(None, None, {node: None for node in self.graph}, set(), set())
            if self.selected_algorithm == "Dijkstra_PQ":
                self.graph_draw_normal.draw_graph_dijkstra(None, None, {node: None for node in self.graph}, set(), set())
            if self.selected_algorithm == "Dijkstra_List":
                self.graph_draw_list.draw_graph_dijkstra_list(None, None, {node: None for node in self.graph}, set(), set())
            if self.steps_finished_algorithm:
                self.gui_frame.cancel_button.config(state=NORMAL)
                self.code_frame.highlight_step("Starting Algorithm")

                if self.selected_algorithm == "Dijkstra_PQ_lazy":
                    self.code_frame.set_step("Starte Dijkstra mit Priority Queue (mit Lazy Deletion)")
                if self.selected_algorithm == "Dijkstra_PQ":
                    self.code_frame.set_step("Starte Dijkstra mit Priority Queue (ohne Lazy Deletion)")
                if self.selected_algorithm == "Dijkstra_List":
                    self.code_frame.set_step("Starte Dijkstra mit Liste")
            return

        self.gui_frame.cancel_button.config(state=NORMAL)
        self.gui_frame.prev_button.config(state=NORMAL)
        step = self.steps_finished_algorithm[self.current_step]
        current_node = step["current_node"]
        neighbor = step["neighbor"]
        distances = step["distances"].copy()

        #Lade entweder eine Priority Queue oder eine Liste, je nach algorithmus.
        if self.selected_algorithm == "Dijkstra_PQ_lazy" or self.selected_algorithm == "Dijkstra_PQ":
            priority_queue = step["priority_queue"].copy()
        else:
            priority_queue = step["list"].copy()

        self.code_frame.update_distances(distances)
        visited = step["visited"].copy()
        visited_edges = step["visited_edges"].copy()
        if self.debug:
            print(step)
        #call different draw graph depending on alg
        if self.selected_algorithm == "Dijkstra_PQ_lazy":
            self.graph_draw_lazy.draw_graph_dijkstra_lazy(current_node, neighbor, distances, visited, visited_edges)

        if self.selected_algorithm == "Dijkstra_PQ":
            self.graph_draw_normal.draw_graph_dijkstra(current_node, neighbor, distances, visited, visited_edges)

        if self.selected_algorithm == "Dijkstra_List":
            self.graph_draw_list.draw_graph_dijkstra_list(current_node, neighbor, distances, visited, visited_edges)


        self.code_frame.highlight(step["step_type"])
        self.code_frame.update_priority_queue(priority_queue)

        if self.shortest_paths:
            if not step["step_type"] == "Algorithm Finished":
                self.gui_frame.shortest_paths_button.config(state=DISABLED)
            else:
                self.gui_frame.shortest_paths_button.config(state=NORMAL)

    #Zeichnet den übergebenen Pfad, need rework still
    def draw_graph_path(self,path):
        self.graph_draw_path = Graph_Visualizer_Path(self.gui_frame, self.node_positions, self.graph, self.start_node, self)
        self.graph_draw_path.draw_path(path)

    #Function um berechnete Distanzen mit networkx Ergebniss zu vergleichen
    def test_dijkstra_algorithm(self, source_node):
        graph_data = self.graph
        G = nx.DiGraph()


        for node, neighbors in graph_data.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)


        print(f"Graph nodes: {list(G.nodes)}")
        print(f"Graph edges: {list(G.edges(data=True))}")
        print(f"Source node: {source_node}")


        if source_node not in G:
            print(f"Error: Source node {source_node} is not in the graph.")
            return False


        computed_distances_nx = nx.single_source_dijkstra_path_length(G, source_node)


        computed_distances_step = self.steps_finished_algorithm[-1]["distances"]

        print("NetworkX computed distances:", computed_distances_nx)
        print("Algorithm computed distances:", computed_distances_step)


        all_nodes = set(computed_distances_nx.keys()).union(set(computed_distances_step.keys()))
        for node in all_nodes:
            expected_distance = computed_distances_nx.get(node, float('inf'))
            computed_distance_step = computed_distances_step.get(node, float('inf'))

            if computed_distance_step != expected_distance:
                print(f"Test failed for node {node}: expected {expected_distance}, got {computed_distance_step}")
                return False

        print("All tests passed.")
        return True



