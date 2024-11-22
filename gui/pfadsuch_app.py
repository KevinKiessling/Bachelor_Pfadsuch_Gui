from tkinter import *
from gui.frame import *
from gui.pseudocode_frame import *
from algorithmen.dijkstra_pq import *
from algorithmen.dijkstra_list import *
import math
class PfadsuchApp(Tk):
    def __init__(self):
        super().__init__()

        #debug mode
        self.debug = True


        self.graph = {}
        self.start_node = '1'
        self.steps = []
        self.current_step = -1
        self.node_creation_mode = False
        self.edge_creation_mode = False

        self.node_positions = {}
        self.selected_nodes = []
        self.selected_algorithm = True # True für dijkstra mit Liste, false für Priority queue


        #titel
        self.title("Eine Gui zur Visualisierung von Pfadsuch-Algorithmen")
        self.geometry('1500x1000')

        # Auslagern der Gui erstellung in andere Klasse
        self.gui_frame = My_Frame(self)
        self.code_frame = Pseudocode_Frame(self)

        #initialisiere Dijkstra

        if self.selected_algorithm == True:
            print("dijkstra mit List")
            self.dijkstra_l = Dijkstra_List()
            self.dijkstra_l.run_dijkstra_list(self.graph)

        else:
            print("dijkstra mit pq")
            self.dijkstra_pq = Dijkstra_Pq()
            self.dijkstra_pq.run_dijkstra_pq(self.graph)


        self.load_default_graph()
        #self.update_gui()

    def next_step(self):
        if self.debug:
            print("TODO:next step")

        if self.current_step < len(self.steps) -1:
            self.current_step += 1
            self.update_gui()


    def prev_step(self):
        if self.debug:
            print("TODO:prev step")

        if self.current_step > -1:
            self.current_step -= 1
            self.update_gui()

    def fast_forward(self):
        if self.debug:
            print("TODO:fast forward")
        if self.current_step < len(self.steps) -1:
            self.current_step += 1
            self.update_gui()
            self.after(500,self.fast_forward)


    def pause(self):
        if self.debug:
            print("TODO:pausing")


    # Läd default graph beim starten der App und auf wunsch
    def load_default_graph(self):
        if self.debug:
            print("Loading default graph")
        self.graph = {'1': {'2': 100, '3': 100, '4': 100}, '2': {'4': 100, '5': 100}, '3': {'4': 100, '2': 100}, '4': {}, '5': {'1': 100}}
        self.node_positions = {'1': (260, 216), '2': (739, 218), '3': (290, 673), '4': (828, 698), '5': (551, 898)}
        self.start_node = '1'
        self.selected_nodes = []
        self.reset()

    #Setzt den Algorithmus komplett zurück, aber behält den Graph geladen
    def reset(self):
        if self.debug:
            print("resetting without clear")
        self.steps = []
        self.current_step = -1

        self.update_gui()

        #self.dijkstra_algorithm.run_dijkstra()


    #Setzt alles zurück und löscht auch den geladenen Graph
    def clear_graph(self):
        if self.debug:
            print("clearing everything")
        self.graph = {}
        self.steps = []
        self.current_step = -1
        self.node_positions = {}
        self.selected_nodes = []
        self.update_gui()

    # Gui Update hier wird der on Screen stuff generiert Später
    def update_gui(self):
       # self.reset()
        self.draw_graph()


    #zeichnet den Graph
    def draw_graph(self):
        print("Drawing Graph")
        self.gui_frame.canvas.delete("all")
        node_radius = 30  # Knoten Größe
        font_size = 16
        already_drawn_edges = set()
        #basic draw node
        for node, (x, y) in self.node_positions.items():

            #hightlightet aktuell ausgewählten knoten für kanten erstellung
            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="green")
                self.gui_frame.canvas.create_text(x, y, text=node, fill="black", font=("Arial", font_size))
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
                self.gui_frame.canvas.create_text(x, y, text=node, fill="black", font=("Arial", font_size))


        # Zeichne alle Kanten, dabei wird zwischen 2 Varianten unterschieden, Direkt oder Bidirekt
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():

                #falls kante schonmal behandelt wurde, skip
                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue

                if neighbor in self.node_positions:
                    #Knoten Positionen
                    x1, y1 = self.node_positions[node]
                    x2, y2 = self.node_positions[neighbor]

                    # berechnet offset, damit kanten nicht in die knoten clippen
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


                    #Kante teilen um das Gewicht zu zeigen
                    middle_space = 0.12  # platz für das gewicht in der mitte

                    segment_dx = dx / distance * middle_space * distance
                    segment_dy = dy / distance * middle_space * distance

                    #Erkenne ob die Kante Bidirektional ist um sie anders zu zeichnen
                    is_bidirectional = neighbor in self.graph and node in self.graph[neighbor]
                   # print(is_bidirectional)

                    if is_bidirectional:

                        # Offset um die bidirektionale kante einzufügen
                        offset = 10
                        # Beide Kanten auseinander "Ziehen"
                        perp_dx = -dy / distance * offset
                        perp_dy = dx / distance * offset
                        # 1. Kante koordinaten
                        x1_offset = x1_no_node_clip + perp_dx
                        y1_offset = y1_no_node_clip + perp_dy
                        x2_offset = x2_no_node_clip + perp_dx
                        y2_offset = y2_no_node_clip + perp_dy
                        middle_x = (x1_offset + x2_offset) / 2
                        middle_y = (y1_offset + y2_offset) / 2
                        #print(x1_offset, x2_offset, y1_offset, y2_no_node_clip)

                        # Kante in 2 teile trennen
                        self.gui_frame.canvas.create_line(
                            x1_offset, y1_offset, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=3, tags="edge"
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_offset, y2_offset,
                            width=3, tags="edge", arrow="last", arrowshape=(10, 12, 5)
                        )
                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=str(weight), fill="black", font=("Arial", 14), tags="weight"
                        )

                        #offset für die 2. Kante
                        x1_offset = x1_no_node_clip - perp_dx
                        y1_offset = y1_no_node_clip - perp_dy
                        x2_offset = x2_no_node_clip - perp_dx
                        y2_offset = y2_no_node_clip - perp_dy
                        #print(x1_offset, x2_offset, y1_offset, y2_no_node_clip)
                        middle_x = (x1_offset + x2_offset) / 2
                        middle_y = (y1_offset + y2_offset) / 2

                        # Kante in 2 Teile trennen
                        self.gui_frame.canvas.create_line(
                            x2_offset, y2_offset, middle_x + segment_dx / 2, middle_y + segment_dy / 2,
                            width=3, tags="edge"
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x - segment_dx / 2, middle_y - segment_dy / 2, x1_offset, y1_offset,
                            width=3, tags="edge", arrow="last", arrowshape=(10, 12, 5)
                        )
                        #gewicht in die Mitte schreiben
                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y, text=str(self.graph[neighbor][node]), font=("Arial", 14), tags="weight"
                        )
                    #zeichne normale kante
                    else:

                        # Einzelne Kante auch wieder mittig teilen für das Gewicht
                        middle_x = (x1_no_node_clip + x2_no_node_clip) / 2
                        middle_y = (y1_no_node_clip + y2_no_node_clip) / 2

                        self.gui_frame.canvas.create_line(
                            x1_no_node_clip, y1_no_node_clip, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                            width=3, tags="edge"
                        )
                        self.gui_frame.canvas.create_line(
                            middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2_no_node_clip, y2_no_node_clip,
                            width=3, tags="edge", arrow="last", arrowshape=(10, 12, 5)
                        )
                        self.gui_frame.canvas.create_text(
                            middle_x, middle_y,
                            text=str(weight),
                            fill="black",
                            font=("Arial", 14),
                            tags="weight"
                        )
                    # Speichere Kanten die bereits gezeichnet wurden, damit bidirektionale kanten nicht 4x gezeichnet werden
                    already_drawn_edges.add((node, neighbor))



