import json
from tkinter import *
from tkinter import messagebox
from gui.frame import *
from gui.pseudocode_frame import *
from algorithmen.dijkstra_list import *
from algorithmen.dijkstra_Priority_queue_lazy import *
from algorithmen.dijkstra_Priority_queue import *
from graph_visualizer.graph_visualizer_dijkstra_lazy import *
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
        self.selected_datastructure_view = StringVar(value="Priority Queue")

        self.fast_forward_paused = False
        self.node_positions = {}
        self.selected_nodes = []
        self.selected_algorithm = "Dijkstra_PQ_lazy"

        #farben für highlighting im pseudocode und in Graph
        self.color_heap = "#d2cd6f"
        self.color_d_v = "violet"
        self.color_d_u = "yellow"
        self.color_discovered_true = "00ff40"
        self.color_discovered_false = "orange"
        self.color_default = "yellow"
        self.color_edge_highlight = "#4ecdf8"

        #zum ausgrauen
        self.color_greyed = "light grey"

        self.visited_edge_color = "lawn green"
        self.highlighted_edge_color = "red"
        self.visited_node_color = "lawn green"
        self.current_node_color = "yellow"
        self.path_color = "light blue"


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

                self.visited_edge_color = config.get("visited_edge_color", self.visited_edge_color)
                self.highlighted_edge_color = config.get("highlighted_edge_color", self.highlighted_edge_color)
                self.visited_node_color = config.get("visited_node_color", self.visited_node_color)
                self.current_node_color = config.get("current_node_color", self.current_node_color)
                self.path_color = config.get("path_color", self.path_color)
                self.font_size = config.get("font_size", self.font_size)

                loaded_value = config.get("selected_datastructure_view", self.selected_datastructure_view)


                self.selected_datastructure_view = StringVar(value=loaded_value)

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
            "visited_edge_color": self.visited_edge_color,
            "highlighted_edge_color": self.highlighted_edge_color,
            "visited_node_color": self.visited_node_color,
            "current_node_color": self.current_node_color,
            "path_color": self.path_color,
            "font_size": self.font_size,
            "selected_datastructure_view": self.selected_datastructure_view.get()

           # "darkmode": self.darkmode
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
        self.gui_frame.canvas.delete("all")

        if self.current_step == -1:
            if self.selected_algorithm == "Dijkstra_PQ_lazy":
                self.graph_draw_lazy.draw_graph_dijkstra_lazy(None, None, {node: 0 for node in self.graph}, set(), set())
            if self.selected_algorithm == "Dijkstra_PQ":
                self.draw_graph_dijkstra_normal(None, None, {node: 0 for node in self.graph}, set(), set())
            if self.selected_algorithm == "Dijkstra_List":
                self.draw_graph_dijkstra_list(None, None, {node: 0 for node in self.graph}, set(), set())
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
            if step["step_type"] == "Algorithm Finished":
                self.draw_graph_dijkstra_normal(None, None, distances, visited, visited_edges)

                self.code_frame.update_priority_queue(priority_queue)
                if self.debug:
                    print(distances)
                if self.shortest_paths:
                    self.gui_frame.shortest_paths_button.config(state=NORMAL)
                return
            else:
                self.draw_graph_dijkstra_normal(current_node, neighbor, distances, visited, visited_edges)

        if self.selected_algorithm == "Dijkstra_List":
            if step["step_type"] == "Algorithm Finished":

                self.draw_graph_dijkstra_list(None, None, distances, visited, visited_edges)
                self.code_frame.highlight(step["step_type"])
                self.code_frame.update_priority_queue(priority_queue)
                if self.debug:
                    print(distances)
                if self.shortest_paths:
                    self.gui_frame.shortest_paths_button.config(state=NORMAL)
                return
            if step["step_type"] == "Highlight Edge":
                self.draw_graph_dijkstra_list(current_node, neighbor, distances, visited, visited_edges,)
            else:
                self.draw_graph_dijkstra_list(current_node, neighbor, distances, visited, visited_edges)


        self.code_frame.highlight(step["step_type"])
        self.code_frame.update_priority_queue(priority_queue)

        if self.shortest_paths:
            if not step["step_type"] == "Algorithm Finished":
                self.gui_frame.shortest_paths_button.config(state=DISABLED)
            else:
                self.gui_frame.shortest_paths_button.config(state=NORMAL)


    #zeichnet den Graph
    def draw_graph_dijkstra_normal(self, current_node, neighbor_list, distances, visited, visited_edges, highlight_only_edge=False):
        self.gui_frame.canvas.delete("all")
        node_radius = 30
        font_size = 14
        already_drawn_edges = set()
        print("normal graph")
        #basic draw node
        for node, (x, y) in self.node_positions.items():
            color = "lightblue"
            if node == current_node:
                color = self.current_node_color
            elif node in visited:

                color = self.visited_node_color

            distance_text = distances.get(node, float('inf'))
            distance_text = f"{distance_text if distance_text < float('inf') else '∞'}"

            distance_length = len(distance_text)

            node_length = len(node)
            padding = max(0, distance_length - node_length)

            if distances.get(node, float('inf'))>=9999:
                font_size = 12
                left_padding = (padding + 2) // 2
                right_padding = padding // 2
            else:
                font_size = 14
                left_padding = (padding + 1) // 2  #
                right_padding = padding // 2

            node_text = f"{' ' * left_padding}{node}{' ' * right_padding}"
            display_text = f"{node_text}\n{distance_text}"

            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")

                self.gui_frame.canvas.create_text(
                    x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                )
                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(
                        x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                    )
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill=color)


                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))



        # Zeichne alle Kanten, dabei wird zwischen 2 Varianten unterschieden, Direkt oder Bidirekt
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():

                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue

                edge_color = "black"

                if (node, neighbor) in visited_edges or (neighbor, node) in visited_edges:
                    edge_color = self.visited_edge_color
                if node == current_node and neighbor == neighbor_list:
                    edge_color = self.highlighted_edge_color

                if neighbor in self.node_positions:
                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]

                    dx = x2 - x1
                    dy = y2 - y1
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance > 0:
                        x1_no_node_clip = x1 + dx / distance * node_radius
                        y1_no_node_clip = y1 + dy / distance * node_radius
                        x2_no_node_clip = x2 - dx / distance * node_radius
                        y2_no_node_clip = y2 - dy / distance * node_radius
                    else:
                        x1_no_node_clip, y1_no_node_clip, x2_no_node_clip, y2_no_node_clip = x1, y1, x2, y2

                    middle_space = 0.12

                    segment_dx = dx / distance * middle_space * distance
                    segment_dy = dy / distance * middle_space * distance

                    is_bidirectional = neighbor in self.graph and node in self.graph[neighbor]

                    if is_bidirectional:
                        forward_colour = "black"
                        reverse_colour = "black"

                        if (node, neighbor) in visited_edges:
                            forward_colour = self.visited_edge_color
                        if (neighbor, node) in visited_edges:
                            reverse_colour = self.visited_edge_color
                        if (node == current_node and neighbor == neighbor_list):
                            forward_colour = self.highlighted_edge_color
                        if (neighbor == current_node and node == neighbor_list):
                            reverse_colour = self.highlighted_edge_color

                        offset = 13

                        perp_dx = -dy / distance * offset
                        perp_dy = dx / distance * offset

                        weight_text_forward = str(weight)
                        weight_text_reverse = str(self.graph[neighbor][node])
                        text_width_forward = len(weight_text_forward) * 6
                        text_width_reverse = len(weight_text_reverse) * 6

                        max_text_width = max(text_width_forward, text_width_reverse)

                        middle_space_expanded = middle_space + max_text_width / distance * 1.5

                        segment_dx_expanded = dx / distance * middle_space_expanded * distance
                        segment_dy_expanded = dy / distance * middle_space_expanded * distance


                        x1_offset = x1_no_node_clip + perp_dx
                        y1_offset = y1_no_node_clip + perp_dy
                        x2_offset = x2_no_node_clip + perp_dx
                        y2_offset = y2_no_node_clip + perp_dy
                        middle_x_forward = (x1_offset + x2_offset) / 2 + segment_dx_expanded / 2
                        middle_y_forward = (y1_offset + y2_offset) / 2 + segment_dy_expanded / 2

                        self.gui_frame.canvas.create_line(
                            x1_offset, y1_offset, middle_x_forward - segment_dx_expanded / 2,
                                                  middle_y_forward - segment_dy_expanded / 2,
                            width=4, tags="edge", fill=forward_colour, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x_forward + segment_dx_expanded / 2, middle_y_forward + segment_dy_expanded / 2,
                            x2_offset, y2_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=forward_colour,
                            smooth=True, splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x_forward, middle_y_forward,
                            text=weight_text_forward, fill="black", font=("Arial", 13), tags="weight"
                        )

                        # Reverse edge
                        x1_offset = x1_no_node_clip - perp_dx
                        y1_offset = y1_no_node_clip - perp_dy
                        x2_offset = x2_no_node_clip - perp_dx
                        y2_offset = y2_no_node_clip - perp_dy
                        middle_x_reverse = (x1_offset + x2_offset) / 2 - segment_dx_expanded / 2
                        middle_y_reverse = (y1_offset + y2_offset) / 2 - segment_dy_expanded / 2

                        self.gui_frame.canvas.create_line(
                            x2_offset, y2_offset, middle_x_reverse + segment_dx_expanded / 2,
                                                  middle_y_reverse + segment_dy_expanded / 2,
                            width=4, tags="edge", fill=reverse_colour, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x_reverse - segment_dx_expanded / 2, middle_y_reverse - segment_dy_expanded / 2,
                            x1_offset, y1_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=reverse_colour,
                            smooth=True, splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x_reverse, middle_y_reverse,
                            text=weight_text_reverse, font=("Arial", 13), tags="weight"
                        )

                    else:
                        weight_text = str(weight)
                        text_width = len(weight_text) * 8

                        middle_space += text_width / distance * 1.5

                        segment_dx = dx / distance * middle_space * distance
                        segment_dy = dy / distance * middle_space * distance

                        middle_x = (x1_no_node_clip + x2_no_node_clip) / 2
                        middle_y = (y1_no_node_clip + y2_no_node_clip) / 2

                        available_space = distance * middle_space
                        if text_width > available_space:
                            extra_space = (text_width - available_space) / 2
                            middle_x -= extra_space

                        self.gui_frame.canvas.create_line(
                            x1_no_node_clip, y1_no_node_clip, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=4, tags="edge", fill=edge_color, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_no_node_clip, y2_no_node_clip,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=edge_color, smooth=True,
                            splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=weight_text,
                            fill="black",
                            font=("Arial", 14),
                            tags="weight"
                        )

                        already_drawn_edges.add((node, neighbor))

    # zeichnet graph mit highlighted path zu übergebenem Endknoten
    def draw_graph_path(self, path):
        self.gui_frame.canvas.delete("all")
        node_radius = 30
        font_size = 16
        already_drawn_edges = set()
        distances = self.steps_finished_algorithm[-1]["distances"]
        start_node = None
        target_node = None

        if path:

            start_node = path[0][0]
            target_node = path[-1][1]

        for node, (x, y) in self.node_positions.items():
            if node == start_node:
                color = self.path_color
            elif node == target_node:
                color = self.path_color
            else:
                color = "light grey"

            if self.steps_finished_algorithm:

                distance_text = distances.get(node, float('inf'))
                distance_text = f"{distance_text if distance_text < float('inf') else '∞'}"

                distance_length = len(distance_text)

                node_length = len(node)
                padding = max(0, distance_length - node_length)

                if distances.get(node, float('inf')) >= 9999:
                    font_size = 12
                    left_padding = (padding + 2) // 2
                    right_padding = padding // 2
                else:
                    font_size = 14
                    left_padding = (padding + 1) // 2  #
                    right_padding = padding // 2

                node_text = f"{' ' * left_padding}{node}{' ' * right_padding}"
                display_text = f"{node_text}\n{distance_text}"

            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                                  fill="green")

                self.gui_frame.canvas.create_text(
                    x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                )
                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(
                        x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                    )
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                                  fill=color)

                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))

        # Zeichne alle Kanten, dabei wird zwischen 2 Varianten unterschieden, Direkt oder Bidirekt
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():

                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue

                edge_color = "light grey"

                if (node, neighbor) in path:
                    edge_color = self.path_color

                if neighbor in self.node_positions:

                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]

                    dx = x2 - x1
                    dy = y2 - y1
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance > 0:
                        x1_no_node_clip = x1 + dx / distance * node_radius
                        y1_no_node_clip = y1 + dy / distance * node_radius
                        x2_no_node_clip = x2 - dx / distance * node_radius
                        y2_no_node_clip = y2 - dy / distance * node_radius
                    else:
                        x1_no_node_clip, y1_no_node_clip, x2_no_node_clip, y2_no_node_clip = x1, y1, x2, y2


                    middle_space = 0.12

                    segment_dx = dx / distance * middle_space * distance
                    segment_dy = dy / distance * middle_space * distance

                    is_bidirectional = neighbor in self.graph and node in self.graph[neighbor]

                    if is_bidirectional:
                        forward_colour = "light grey"
                        reverse_colour = "light grey"

                        if (node, neighbor) in path:
                            forward_colour = self.path_color
                        if (neighbor, node) in path:
                            reverse_colour = self.path_color

                        offset = 13

                        perp_dx = -dy / distance * offset
                        perp_dy = dx / distance * offset


                        weight_text_forward = str(weight)
                        weight_text_reverse = str(self.graph[neighbor][node])
                        text_width_forward = len(weight_text_forward) * 6
                        text_width_reverse = len(weight_text_reverse) * 6

                        max_text_width = max(text_width_forward, text_width_reverse)

                        middle_space_expanded = middle_space + max_text_width / distance * 1.5

                        segment_dx_expanded = dx / distance * middle_space_expanded * distance
                        segment_dy_expanded = dy / distance * middle_space_expanded * distance

                        x1_offset = x1_no_node_clip + perp_dx
                        y1_offset = y1_no_node_clip + perp_dy
                        x2_offset = x2_no_node_clip + perp_dx
                        y2_offset = y2_no_node_clip + perp_dy
                        middle_x_forward = (x1_offset + x2_offset) / 2 + segment_dx_expanded / 2
                        middle_y_forward = (y1_offset + y2_offset) / 2 + segment_dy_expanded / 2

                        self.gui_frame.canvas.create_line(
                            x1_offset, y1_offset, middle_x_forward - segment_dx_expanded / 2,
                                                  middle_y_forward - segment_dy_expanded / 2,
                            width=4, tags="edge", fill=forward_colour, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x_forward + segment_dx_expanded / 2, middle_y_forward + segment_dy_expanded / 2,
                            x2_offset, y2_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=forward_colour,
                            smooth=True, splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x_forward, middle_y_forward,
                            text=weight_text_forward, fill="black", font=("Arial", 13), tags="weight"
                        )
                        # Rückwärtskante
                        x1_offset = x1_no_node_clip - perp_dx
                        y1_offset = y1_no_node_clip - perp_dy
                        x2_offset = x2_no_node_clip - perp_dx
                        y2_offset = y2_no_node_clip - perp_dy
                        middle_x_reverse = (x1_offset + x2_offset) / 2 - segment_dx_expanded / 2
                        middle_y_reverse = (y1_offset + y2_offset) / 2 - segment_dy_expanded / 2

                        self.gui_frame.canvas.create_line(
                            x2_offset, y2_offset, middle_x_reverse + segment_dx_expanded / 2,
                                                  middle_y_reverse + segment_dy_expanded / 2,
                            width=4, tags="edge", fill=reverse_colour, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x_reverse - segment_dx_expanded / 2, middle_y_reverse - segment_dy_expanded / 2,
                            x1_offset, y1_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=reverse_colour,
                            smooth=True, splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x_reverse, middle_y_reverse,
                            text=weight_text_reverse, font=("Arial", 13), tags="weight"
                        )

                    else:
                        weight_text = str(weight)
                        text_width = len(weight_text) * 8
                        middle_space += text_width / distance * 1.5

                        segment_dx = dx / distance * middle_space * distance
                        segment_dy = dy / distance * middle_space * distance

                        middle_x = (x1_no_node_clip + x2_no_node_clip) / 2
                        middle_y = (y1_no_node_clip + y2_no_node_clip) / 2

                        available_space = distance * middle_space
                        if text_width > available_space:
                            extra_space = (text_width - available_space) / 2
                            middle_x -= extra_space

                        self.gui_frame.canvas.create_line(
                            x1_no_node_clip, y1_no_node_clip, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=4, tags="edge", fill=edge_color, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_no_node_clip, y2_no_node_clip,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=edge_color, smooth=True,
                            splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=weight_text,
                            fill="black",
                            font=("Arial", 14),
                            tags="weight"
                        )

                    # Speichere Kanten die bereits gezeichnet wurden, damit bidirektionale Kanten nicht 4x gezeichnet werden
                    already_drawn_edges.add((node, neighbor))

    def draw_graph_dijkstra_list(self, current_node, neighbor_list, distances, visited, visited_edges, highlight_only_edge=False):
        self.gui_frame.canvas.delete("all")
        node_radius = 30
        font_size = 14
        already_drawn_edges = set()
        print("list graph")
        #basic draw node
        for node, (x, y) in self.node_positions.items():
            color = "lightblue"
            if node == current_node:
                color = self.current_node_color
            elif node in visited:

                color = self.visited_node_color

            distance_text = distances.get(node, float('inf'))
            distance_text = f"{distance_text if distance_text < float('inf') else '∞'}"

            distance_length = len(distance_text)

            node_length = len(node)
            padding = max(0, distance_length - node_length)

            if distances.get(node, float('inf'))>=9999:
                font_size = 12
                left_padding = (padding + 2) // 2
                right_padding = padding // 2
            else:
                font_size = 14
                left_padding = (padding + 1) // 2  #
                right_padding = padding // 2

            node_text = f"{' ' * left_padding}{node}{' ' * right_padding}"
            display_text = f"{node_text}\n{distance_text}"

            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")

                self.gui_frame.canvas.create_text(
                    x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                )
                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(
                        x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                    )
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill=color)


                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))



        # Zeichne alle Kanten, dabei wird zwischen 2 Varianten unterschieden, Direkt oder Bidirekt
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():

                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue

                edge_color = "black"

                if (node, neighbor) in visited_edges or (neighbor, node) in visited_edges:
                    edge_color = self.visited_edge_color
                if node == current_node and neighbor == neighbor_list:
                    edge_color = self.highlighted_edge_color

                if neighbor in self.node_positions:
                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]

                    dx = x2 - x1
                    dy = y2 - y1
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance > 0:
                        x1_no_node_clip = x1 + dx / distance * node_radius
                        y1_no_node_clip = y1 + dy / distance * node_radius
                        x2_no_node_clip = x2 - dx / distance * node_radius
                        y2_no_node_clip = y2 - dy / distance * node_radius
                    else:
                        x1_no_node_clip, y1_no_node_clip, x2_no_node_clip, y2_no_node_clip = x1, y1, x2, y2

                    middle_space = 0.12

                    segment_dx = dx / distance * middle_space * distance
                    segment_dy = dy / distance * middle_space * distance

                    is_bidirectional = neighbor in self.graph and node in self.graph[neighbor]

                    if is_bidirectional:
                        forward_colour = "black"
                        reverse_colour = "black"

                        if (node, neighbor) in visited_edges:
                            forward_colour = self.visited_edge_color
                        if (neighbor, node) in visited_edges:
                            reverse_colour = self.visited_edge_color
                        if (node == current_node and neighbor == neighbor_list):
                            forward_colour = self.highlighted_edge_color
                        if (neighbor == current_node and node == neighbor_list):
                            reverse_colour = self.highlighted_edge_color

                        offset = 13

                        perp_dx = -dy / distance * offset
                        perp_dy = dx / distance * offset

                        weight_text_forward = str(weight)
                        weight_text_reverse = str(self.graph[neighbor][node])
                        text_width_forward = len(weight_text_forward) * 6
                        text_width_reverse = len(weight_text_reverse) * 6

                        max_text_width = max(text_width_forward, text_width_reverse)

                        middle_space_expanded = middle_space + max_text_width / distance * 1.5

                        segment_dx_expanded = dx / distance * middle_space_expanded * distance
                        segment_dy_expanded = dy / distance * middle_space_expanded * distance


                        x1_offset = x1_no_node_clip + perp_dx
                        y1_offset = y1_no_node_clip + perp_dy
                        x2_offset = x2_no_node_clip + perp_dx
                        y2_offset = y2_no_node_clip + perp_dy
                        middle_x_forward = (x1_offset + x2_offset) / 2 + segment_dx_expanded / 2
                        middle_y_forward = (y1_offset + y2_offset) / 2 + segment_dy_expanded / 2

                        self.gui_frame.canvas.create_line(
                            x1_offset, y1_offset, middle_x_forward - segment_dx_expanded / 2,
                                                  middle_y_forward - segment_dy_expanded / 2,
                            width=4, tags="edge", fill=forward_colour, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x_forward + segment_dx_expanded / 2, middle_y_forward + segment_dy_expanded / 2,
                            x2_offset, y2_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=forward_colour,
                            smooth=True, splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x_forward, middle_y_forward,
                            text=weight_text_forward, fill="black", font=("Arial", 13), tags="weight"
                        )

                        # Reverse edge
                        x1_offset = x1_no_node_clip - perp_dx
                        y1_offset = y1_no_node_clip - perp_dy
                        x2_offset = x2_no_node_clip - perp_dx
                        y2_offset = y2_no_node_clip - perp_dy
                        middle_x_reverse = (x1_offset + x2_offset) / 2 - segment_dx_expanded / 2
                        middle_y_reverse = (y1_offset + y2_offset) / 2 - segment_dy_expanded / 2

                        self.gui_frame.canvas.create_line(
                            x2_offset, y2_offset, middle_x_reverse + segment_dx_expanded / 2,
                                                  middle_y_reverse + segment_dy_expanded / 2,
                            width=4, tags="edge", fill=reverse_colour, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x_reverse - segment_dx_expanded / 2, middle_y_reverse - segment_dy_expanded / 2,
                            x1_offset, y1_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=reverse_colour,
                            smooth=True, splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x_reverse, middle_y_reverse,
                            text=weight_text_reverse, font=("Arial", 13), tags="weight"
                        )

                    else:
                        weight_text = str(weight)
                        text_width = len(weight_text) * 8

                        middle_space += text_width / distance * 1.5

                        segment_dx = dx / distance * middle_space * distance
                        segment_dy = dy / distance * middle_space * distance

                        middle_x = (x1_no_node_clip + x2_no_node_clip) / 2
                        middle_y = (y1_no_node_clip + y2_no_node_clip) / 2

                        available_space = distance * middle_space
                        if text_width > available_space:
                            extra_space = (text_width - available_space) / 2
                            middle_x -= extra_space

                        self.gui_frame.canvas.create_line(
                            x1_no_node_clip, y1_no_node_clip, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=4, tags="edge", fill=edge_color, smooth=True, splinesteps=500
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_no_node_clip, y2_no_node_clip,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=edge_color, smooth=True,
                            splinesteps=500
                        )

                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=weight_text,
                            fill="black",
                            font=("Arial", 14),
                            tags="weight"
                        )

                        already_drawn_edges.add((node, neighbor))




