import json
from tkinter import *
from tkinter import messagebox
from gui.frame import *
from gui.pseudocode_frame import *
from algorithmen.dijkstra_list import *
from algorithmen.dijkstra_Priority_queue_lazy import *
from algorithmen.dijkstra_Priority_queue import *
from graph_visualizer.graph_visualizer_dijkstra_lazy import *
from graph_visualizer.graph_visualizer_dijkstra import *
from graph_visualizer.graph_visualizer_dijkstra_list import *
from graph_visualizer.graph_visualizer_path import *
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

        self.fast_forward_paused = False
        self.node_positions = {}
        self.selected_nodes = []
        self.selected_algorithm = "Dijkstra_PQ_lazy"

        #farben für highlighting im pseudocode und in Graph
        self.color_heap = "#d2cd6f"
        self.color_d_v = "violet"
        self.color_d_u = "yellow"
        self.color_discovered_true = "#00ff40"
        self.color_discovered_false = "orange"
        self.color_default = "yellow"
        self.color_edge_highlight = "#4ecdf8"
        self.color_shortest_path = "light blue"

        self.title("Eine Gui zur Visualisierung von Pfadsuch-Algorithmen")
        self.geometry('1850x1100')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)


        self.bind_all("<FocusIn>", self.global_focus_control)

        self.code_frame = Pseudocode_Frame(self)
        self.gui_frame = My_Frame(self)


        self.load_config()
        self.load_default_graph()
        self.code_frame.update_font_size()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

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


                self.debug = config.get("debug", self.debug)
                self.random_edge_mode = config.get("random_edge_mode", self.random_edge_mode)
                self.animation_speed = config.get("animation_speed", self.animation_speed)
                self.default_graph = config.get("default_graph", self.default_graph)
                self.default_graph_pos = config.get("default_graph_pos", self.default_graph_pos)
                self.max_edge_weight = config.get("max_edge_weight", self.max_edge_weight)

                self.color_heap = config.get("color_heap", self.color_heap)
                self.color_d_v = config.get("color_d_v", self.color_d_v)
                self.color_d_u = config.get("color_d_u", self.color_d_u)
                self.color_discovered_true = config.get("color_discovered_true", self.color_discovered_true)
                self.color_discovered_false = config.get("color_discovered_false", self.color_discovered_false)
                self.color_default = config.get("color_default", self.color_default)
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
            "debug": self.debug,
            "random_edge_mode": self.random_edge_mode,
            "animation_speed": self.animation_speed,
            "default_graph_pos": self.default_graph_pos,
            "default_graph": self.default_graph,
            "max_edge_weight": self.max_edge_weight,
            "color_heap": self.color_heap,
            "color_d_v": self.color_d_v,
            "color_d_u": self.color_d_u,
            "color_discovered_true": self.color_discovered_true,
            "color_discovered_false": self.color_discovered_false,
            "color_default": self.color_default,
            "color_edge_highlight": self.color_edge_highlight,
            "color_shortest_path": self.color_shortest_path,
        }
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        #self.update_gui()
        self.code_frame.update_font_size()
    def start_algorithm(self):
        if self.current_step:
            self.steps_finished_algorithm = []
            self.code_frame.clear_highlights_and_Canvas()
            self.current_step = -1
            self.code_frame.clear_table()
           # self.code_frame.clear_hightlight()

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
        #if self.shortest_paths:
         #   self.gui_frame.shortest_paths_button.config(state=NORMAL)


    def set_starting_node(self, node):
        self.start_node = node
        self.selected_nodes = []
        if self.debug:
            print(f" Knoten {node} als Startknoten gesetzt")
        self.update_gui()

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
        if self.steps_finished_algorithm == []:
            self.start_algorithm()
        if self.fast_forward_paused:
            return
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
        if self.debug:
            print("fast forward stopped bei schritt : ", self.current_step)



    # Läd default graph beim starten der App und auf wunsch
    def load_default_graph(self):
        if self.default_graph:
            self.graph = copy.deepcopy(self.default_graph)
            self.node_positions = copy.deepcopy(self.default_graph_pos)
            self.selected_nodes = []

        else:
            if self.debug:
                print("Loading backup default graph")
            self.graph = {"A": {"E": 1, "B": 2, "K": 5, "I": 5}, "B": {"C": 6}, "C": {"M": 2}, "D": {"C": 2},
                          "E": {"G": 10, "D": 1}, "F": {"D": 9}, "G": {"F": 4, "H": 16}, "H": {"J": 4},
                          "I": {"H": 12, "G": 4}, "J": {}, "K": {"L": 4, "M": 12}, "L": {"J": 42}, "M": {}}
            self.node_positions = {"A": [412, 433], "B": [549, 278], "C": [786, 222], "D": [455, 96], "E": [291, 248],
                                   "F": [73, 102], "G": [48, 488], "H": [112, 815], "I": [426, 678], "J": [657, 949],
                                   "K": [756, 453], "L": [831, 723], "M": [956, 364]}

            self.selected_nodes = []
        self.gui_frame.update_avai_ids()
        self.gui_frame.operation_history = []
        self.reset()

    #Setzt den Algorithmus komplett zurück, aber behält den Graph geladen
    def reset(self):
        if self.debug:
            print("resetting without clear")
        self.steps_finished_algorithm = []
        self.current_step = -1
        self.start_node = ""
        self.update_gui()
        self.code_frame.clear_highlights_and_Canvas()

        self.code_frame.clear_table()
        #TO DO CLEAR TABLE HIGHLIGHT
        #self.code_frame.clear_hightlight()

        self.code_frame.set_step("")
        self.shortest_paths = {}
        if not self.shortest_paths:
            self.gui_frame.shortest_paths_button.config(state=DISABLED)
            self.gui_frame.prev_button.config(state=DISABLED)
        if self.selected_algorithm in {"Dijkstra_PQ_lazy", "Dijkstra_PQ"}:
            self.code_frame.priority_queue_label.config(text="Heap")
            #self.code_frame.priority_queue_table.heading("Node", text="Knoten")
            #self.code_frame.priority_queue_table.heading("Priority", text="Priorität")
        elif self.selected_algorithm == "Dijkstra_List":
            self.code_frame.priority_queue_label.config(text="Liste")
            #self.code_frame.priority_queue_table.heading("Node", text="Knoten")
            #self.code_frame.priority_queue_table.heading("Priority", text="Distanz")



    #Setzt alles zurück und löscht auch den geladenen Graph
    def clear_graph(self):
        if self.debug:
            print("clearing everything")
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
        self.update_gui()

    # Updated die Gui
    def update_gui(self):

        self.graph_draw_lazy = Graph_Visualizer_Dijkstra_lazy(self.gui_frame, self.node_positions, self.graph, self.selected_nodes, self.start_node, self)
        self.graph_draw_normal = Graph_Visualizer_Dijkstra(self.gui_frame, self.node_positions, self.graph, self.selected_nodes, self.start_node, self)
        self.graph_draw_list = Graph_Visualizer_Dijkstra_List(self.gui_frame, self.node_positions, self.graph,
                                                           self.selected_nodes, self.start_node, self)
        self.gui_frame.canvas.delete("all")
        self.gui_frame.prev_button.config(state=DISABLED)
        if self.current_step == -1:
            if self.selected_algorithm == "Dijkstra_PQ_lazy":
                self.graph_draw_lazy.draw_graph_dijkstra_lazy(None, None, {node: 0 for node in self.graph}, set(), set())
            if self.selected_algorithm == "Dijkstra_PQ":
                self.graph_draw_normal.draw_graph_dijkstra(None, None, {node: 0 for node in self.graph}, set(), set())
            if self.selected_algorithm == "Dijkstra_List":
                self.graph_draw_list.draw_graph_dijkstra_list(None, None, {node: 0 for node in self.graph}, set(), set())
            if self.steps_finished_algorithm:
                self.code_frame.highlight_step("Starting Algorithm")
                #self.code_frame.highlight_lines_with_dimming([2])
                if self.selected_algorithm == "Dijkstra_PQ_lazy":
                    self.code_frame.set_step("Starte Dijkstra mit Priority Queue (mit Lazy Deletion)")
                if self.selected_algorithm == "Dijkstra_PQ":
                    self.code_frame.set_step("Starte Dijkstra mit Priority Queue (ohne Lazy Deletion)")
                if self.selected_algorithm == "Dijkstra_List":
                    self.code_frame.set_step("Starte Dijkstra mit Liste")
            return

        self.gui_frame.prev_button.config(state=NORMAL)
        step = self.steps_finished_algorithm[self.current_step]
        current_node = step["current_node"]
        neighbor = step["neighbor"]
        distances = step["distances"].copy()
        priority_queue = step["priority_queue"].copy()
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
        self.graph_draw_path = Graph_Visualizer_Path(self.gui_frame, self.node_positions, self.graph, self.selected_nodes, self.start_node, self)
        self.graph_draw_path.draw_path(path)



