from tkinter import *
from tkinter import messagebox
from gui.frame import *
from gui.pseudocode_frame import *
from algorithmen.dijkstra_list import *
from algorithmen.dijkstra_Priority_queue import *
import math
class PfadsuchApp(Tk):
    def __init__(self):
        super().__init__()

        #debug mode
        self.debug = True
        self.steps_finished_algorithm = []

        self.graph = {}
        self.start_node = ''
        #self.steps = []
        self.current_step = -1


        # um den pause button zu implementieren
        self.fast_forward_paused = False
        self.node_positions = {}
        self.selected_nodes = []
        self.selected_algorithm = "Dijkstra_PQ"


        #titel
        self.title("Eine Gui zur Visualisierung von Pfadsuch-Algorithmen")
        self.geometry('1850x1100')

        # Auslagern der Gui erstellung in andere Klasse
        self.code_frame = Pseudocode_Frame(self)
        self.gui_frame = My_Frame(self)
        self.bind_all("<FocusIn>", self.global_focus_control)
        self.load_default_graph()
        #

    def global_focus_control(self, event):
        if event.widget in self.code_frame.winfo_children():
            self.gui_frame.focus_set()


        #self.update_gui()
    def start_algorithm(self):
        if self.start_node is None or self.start_node == '':
            start_node = tkinter.simpledialog.askstring("Input starting node", "Input starting node")
            self.selected_nodes = []
            if start_node is None:
                return
            if start_node not in self.graph:
                messagebox.showerror("Invalid Node", "The starting node does not exist in the graph.")
                return
            self.start_node = str(start_node)
        if self.selected_algorithm == "Dijkstra_PQ":
            self.dijkstra_pq = Dijkstra_Priority_Queue()
            self.update_gui()
            self.steps_finished_algorithm = self.dijkstra_pq.run_dijkstra_list(self.graph, self.start_node)
            print(self.steps_finished_algorithm)

        if self.selected_algorithm == "Dijkstra_List":
            print("not implemented yet")





    def next_step(self):
        if self.debug:
            print("next step")
        if self.steps_finished_algorithm == []:
            print("no algorithm loaded")

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

    def fast_forward(self):
        if self.debug:
            print("fast forward")
        if self.steps_finished_algorithm == []:
            if self.debug:
                print("no algorithm loaded")
        if self.fast_forward_paused:
            return
        if self.current_step < len(self.steps_finished_algorithm) -1:
            self.current_step += 1
            self.update_gui()
            self.after(500, self.fast_forward)
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
        if self.debug:
            print("Loading default graph")
        self.graph = {'1': {'2': 100, '3': 100, '4': 100}, '2': {'4': 100, '5': 100}, '3': {'4': 100, '2': 100}, '4': {}, '5': {'1': 100}}
        self.node_positions = {'1': (260, 216), '2': (739, 218), '3': (290, 673), '4': (828, 698), '5': (551, 898)}
        self.selected_nodes = []

        self.reset()

    #Setzt den Algorithmus komplett zurück, aber behält den Graph geladen
    def reset(self):
        if self.debug:
            print("resetting without clear")
        self.steps_finished_algorithm = []
        self.current_step = -1
        self.start_node = ""
        self.update_gui()




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
        self.update_gui()

    # Gui Update hier wird der on Screen stuff generiert Später
    def update_gui(self):

        self.gui_frame.canvas.delete("all")

        if self.current_step == -1:
            self.draw_graph(None, None, {node: 0 for node in self.graph}, set(), set())
            return

        step = self.steps_finished_algorithm[self.current_step]
        current_node = step["current_node"]
        neighbor = step["neighbor"]
        distances = step["distances"]
        priority_queue = step["priority_queue"]
        self.code_frame.update_distances(distances)
        visited = step["visited"]
        visited_edges = step["visited_edges"]
        print(step)
        if step["step_type"] == "Algorithm Finished":
            self.draw_graph(None, None, distances, visited, visited_edges)
            print(distances)
            return
        if step["step_type"] == "Highlight Edge":
            self.draw_graph(current_node, neighbor, distances, visited, visited_edges, highlight_only_edge=True)
        else:
            self.draw_graph(current_node, neighbor, distances, visited, visited_edges)

    #zeichnet den Graph
    def draw_graph(self, current_node, neighbor_list, distances, visited, visited_edges, highlight_only_edge=False):
        self.gui_frame.canvas.delete("all")
        node_radius = 30
        font_size = 16
        already_drawn_edges = set()

        #basic draw node
        for node, (x, y) in self.node_positions.items():
            color = "lightblue"
            if node == current_node:
                color = "yellow"
            elif node in visited:
                color = "lawn green"


            #hightlightet aktuell ausgewählten knoten für kanten erstellung
            distance_text = distances.get(node, float('inf'))
            display_text = f"{node}\n{distance_text if distance_text < float('inf') else 'inf'}"

            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")

                self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))
                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill=color)


                if node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))



        # Zeichne alle Kanten, dabei wird zwischen 2 Varianten unterschieden, Direkt oder Bidirekt
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():
                # Falls Kante schonmal behandelt wurde, skip
                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue


                edge_color = "black"

                if (node, neighbor) in visited_edges or (neighbor, node) in visited_edges:

                    edge_color = "lawn green"
                if node == current_node and neighbor == neighbor_list:
                    edge_color = "red"

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

                    # Kante teilen um das Gewicht zu zeigen
                    middle_space = 0.12

                    segment_dx = dx / distance * middle_space * distance
                    segment_dy = dy / distance * middle_space * distance

                    # Erkenne ob die Kante Bidirektional ist, um sie anders zu zeichnen
                    is_bidirectional = neighbor in self.graph and node in self.graph[neighbor]

                    if is_bidirectional:

                        forward_colour = "black"
                        reverse_colour = "black"


                        if (node, neighbor) in visited_edges:
                            forward_colour = "lawn green"
                        if (neighbor, node) in visited_edges:
                            reverse_colour = "lawn green"
                        if (node == current_node and neighbor == neighbor_list):
                            forward_colour = "red"
                        if (neighbor == current_node and node == neighbor_list):
                            reverse_colour = "red"

                        # Offset um die bidirektionale Kante einzufügen
                        offset = 10
                        # Beide Kanten auseinander "ziehen"
                        perp_dx = -dy / distance * offset
                        perp_dy = dx / distance * offset

                        # 1. Kante Koordinaten
                        x1_offset = x1_no_node_clip + perp_dx
                        y1_offset = y1_no_node_clip + perp_dy
                        x2_offset = x2_no_node_clip + perp_dx
                        y2_offset = y2_no_node_clip + perp_dy
                        middle_x = (x1_offset + x2_offset) / 2
                        middle_y = (y1_offset + y2_offset) / 2

                        # Kante in 2 Teile trennen
                        self.gui_frame.canvas.create_line(
                            x1_offset, y1_offset, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=4, tags="edge", fill=forward_colour, smooth=True, splinesteps=300
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_offset, y2_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=forward_colour, smooth=True, splinesteps=300
                        )
                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=str(weight), fill="black", font=("Arial", 14), tags="weight"
                        )

                        # Offset für die 2. Kante
                        x1_offset = x1_no_node_clip - perp_dx
                        y1_offset = y1_no_node_clip - perp_dy
                        x2_offset = x2_no_node_clip - perp_dx
                        y2_offset = y2_no_node_clip - perp_dy
                        middle_x = (x1_offset + x2_offset) / 2
                        middle_y = (y1_offset + y2_offset) / 2




                        # Kante in 2 Teile trennen
                        self.gui_frame.canvas.create_line(
                            x2_offset, y2_offset, middle_x + segment_dx / 2, middle_y + segment_dy / 2,
                            width=4, tags="edge", fill=reverse_colour, smooth=True, splinesteps=300
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x - segment_dx / 2, middle_y - segment_dy / 2, x1_offset, y1_offset,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=reverse_colour, smooth=True, splinesteps=300
                        )

                        # Gewicht in die Mitte schreiben
                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y, text=str(self.graph[neighbor][node]), font=("Arial", 14), tags="weight"
                        )
                    else:
                        # Zeichne normale Kante
                        middle_x = (x1_no_node_clip + x2_no_node_clip) / 2
                        middle_y = (y1_no_node_clip + y2_no_node_clip) / 2

                        self.gui_frame.canvas.create_line(
                            x1_no_node_clip, y1_no_node_clip, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=4, tags="edge", fill=edge_color, smooth=True, splinesteps=300
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_no_node_clip, y2_no_node_clip,
                            width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5), fill=edge_color, smooth=True, splinesteps=300
                        )
                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=str(weight),
                            fill="black",
                            font=("Arial", 14),
                            tags="weight"
                        )

                    # Speichere Kanten die bereits gezeichnet wurden, damit bidirektionale Kanten nicht 4x gezeichnet werden
                    already_drawn_edges.add((node, neighbor))

