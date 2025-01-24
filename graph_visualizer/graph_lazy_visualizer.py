import json
from tkinter import *
from tkinter import messagebox
from gui.frame import *
from gui.pseudocode_frame import *
from algorithmen.dijkstra_list import *
from algorithmen.dijkstra_Priority_queue_lazy import *
from algorithmen.dijkstra_Priority_queue import *

import math

class Graph_Visualizer_lazy:
    def __init__(self, gui_frame, node_positions, graph,selected_nodes, start_node, parent):
        self.gui_frame = gui_frame
        self.node_positions = node_positions
        self.graph = graph
        self.parent = parent
        self.selected_nodes = selected_nodes
        self.start_node = start_node



    def draw_graph_dijkstra_lazy(self, current_node, neighbor_list, distances, visited, visited_edges):
        self.gui_frame.canvas.delete("all")
        node_radius = 30
        font_size = 14
        already_drawn_edges = set()
        color = "lightblue"
        step = {}
        if self.parent.current_step != -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]
            print(step)


        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            # color nodes based on steptype
            if step:
                # wenn alg. durchgelaufen, dann sind alle Knoten hellblau
                if step["step_type"] == "Algorithm Finished":
                    color = "light blue"
                # wenn Knoten während initialisierung gewählt wird, dann ist dieser Knoten gelb. Rest ist grau
                if step["step_type"] == "Pick Node":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"
                #  NEEDS WORK!! Aktueller Knoten gelb, sonst grau
                if step["step_type"] == "Initialize Node Distance":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"
                # StartKnoten gelb, rest grau
                if step["step_type"] == "Set Start Node Distance":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"
                # StartKnoten wird auf PQ pushed, also alles grau ausser startKnoten #57b3ea für hellblau
                if step["step_type"] == "Push Start Node to Priority Queue":
                    color = "light grey"
                    if node == current_node:
                        color = "#57b3ea"
                # Knoten im Heap  sind blau, aus Heap entfernter Knoten ist gelb, rest grau
                if step["step_type"] == "Heap Pop":
                    color = "light grey"
                    if any(n == node for _, n in step["priority_queue"]):
                        color = "#57b3ea"
                    if node == current_node:
                        color = "yellow"

                # NEEDS WORK!! Füge current node den Discoverten Nodes hinzu, visited nodes = grün, aktueller = #4bf569, rest grau
                if step["step_type"] == "Visit Node":
                    color = "light grey"
                    if node in visited:
                        color = "#00ff40"
                    if node == current_node:
                        color = "lime green"

                # NEEDS WORK!! vergleiche Distanzen also alles bis auf Current node und aktueller nachbar gray, die beiden sind gelb
                if step["step_type"] == "Compare Distance":
                    color = "light grey"
                    if node == current_node or node in neighbor_list:
                        color = "yellow"

                # Aktueller Knoten gelb, rest grau.
                if step["step_type"] == "Highlight Edge":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"

                #Färbe Knoten die in Queue sind #57b3ea, rest grau
                if step["step_type"] == "Begin Outer Loop":
                    color = "light grey"
                    if any(n == node for _, n in step["priority_queue"]):
                        color = "#57b3ea"

                # Aktueller Knoten gelb, rest grau, hier werden nur alle Kanten highlighted
                if step["step_type"] == "Begin Inner Loop":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"
                # Update Distanzen von Nachbar und pushe ihn auf Heap, aktueller Knoten gelb, Nachbar #57b3ea, rest grau
                if step["step_type"] == "Update Distance and Push to Heap":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"
                    if node in neighbor_list:
                        color = "#57b3ea"

                # Überspringe besuchte Knoten
                if step["step_type"] == "Skip Visited Node":
                    color = "light grey"
                    if node in visited:
                        color = "#00ff40"
                    if node == current_node:
                        color = "lime green"

                # Überspringe besuchte Nachbarn
                if step["step_type"] == "Skip Visited Neighbor":
                    color = "light grey"
                    if node == current_node:
                        color = "yellow"
                    if node in neighbor_list:
                        color = "#00ff40"

                #Priority Queue is leer, alles gray
                if step["step_type"] == "Priority Queue Empty":
                    color = "light grey"


            #Knoten werte
            distance_text = distances.get(node, 0)
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
                left_padding = (padding + 1) // 2
                right_padding = padding // 2

            node_text = f"{' ' * left_padding}{node}{' ' * right_padding}"
            display_text = f"{node_text}\n{distance_text}"
            # Flag to display "start" on start node
            show_start = True
            #chbange node display text
            if step:

                # Show distances and node Name when finished
                if step["step_type"] == "Algorithm Finished":
                    show_start = True
                # Zeige nur node Name+ distanz, kein Start
                if step["step_type"] == "Pick Node":
                    show_start = False
                # Zeige Distanzen, kein Start
                if step["step_type"] == "Initialize Node Distance":
                    show_start = False
                #  Zeige Distanzen, kein Start
                if step["step_type"] == "Set Start Node Distance":
                    show_start = False
                #  Zeige Distanzen, kein Start
                if step["step_type"] == "Push Start Node to Priority Queue":
                    show_start = False

                if step["step_type"] == "Heap Pop":
                    show_start = False
                if step["step_type"] == "Visit Node":
                    show_start = False
                if step["step_type"] == "Compare Distance":
                    show_start = False
                if step["step_type"] == "Highlight Edge":
                    show_start = False
                if step["step_type"] == "Begin Outer Loop":
                    show_start = False
                if step["step_type"] == "Begin Inner Loop":
                    show_start = False
                if step["step_type"] == "Update Distance and Push to Heap":
                    show_start = False
                if step["step_type"] == "Skip Visited Node":
                    show_start = False
                if step["step_type"] == "Skip Visited Neighbor":
                    show_start = False
                if step["step_type"] == "Priority Queue Empty":
                    show_start = False



            if node in self.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                                  fill="green")
                self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size),
                                                  anchor="center")
                if show_start and node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                                  fill=color)
                if show_start and node == self.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))

        # Draw edges
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():

                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue

                edge_color = "black"
                #change edge color depending on state
                if step:
                    #Algorithmus durch = Kanten normal Black
                    if step["step_type"] == "Algorithm Finished":
                        edge_color = "black"
                    # Kanten ausgegraut
                    if step["step_type"] == "Pick Node":
                        edge_color = "light grey"
                    # Kanten ausgegraut
                    if step["step_type"] == "Initialize Node Distance":
                        edge_color = "light grey"
                    # Kanten ausgegraut
                    if step["step_type"] == "Set Start Node Distance":
                        edge_color = "light grey"
                    # Kanten ausgegraut
                    if step["step_type"] == "Push Start Node to Priority Queue":
                        edge_color = "light grey"
                    # Kanten ausgegraut
                    if step["step_type"] == "Heap Pop":
                        edge_color = "light grey"
                    # Kanten ausgegraut
                    if step["step_type"] == "Visit Node":
                        edge_color = "light grey"
                    # Aktuelle Kante ist grün, rest grau
                    if step["step_type"] == "Compare Distance":
                        edge_color = "light grey"
                        if node == current_node and neighbor == neighbor_list:
                            edge_color = "light green"

                    # Aktuelle Kante ist grün, rest grau
                    if step["step_type"] == "Highlight Edge":
                        edge_color = "light grey"
                        if node == current_node and neighbor == neighbor_list:
                            edge_color = "light green"
                    # Kanten ausgegraut
                    if step["step_type"] == "Begin Outer Loop":
                        edge_color = "light grey"

                    # highlighte alle ausgehenden Kanten von current Node, rot nicht bearbeitet, grün bearbeitet
                    if step["step_type"] == "Begin Inner Loop":
                        if (node, neighbor) in visited_edges and node == current_node:
                            edge_color = "light green"
                        elif node == current_node:
                            edge_color = "red"
                        else:
                            edge_color = "light grey"

                    # Kanten ausgegraut
                    if step["step_type"] == "Update Distance and Push to Heap":
                        edge_color = "light grey"

                    # Kanten ausgegraut
                    if step["step_type"] == "Skip Visited Node":
                        edge_color = "light grey"

                    if step["step_type"] == "Skip Visited Neighbor":
                        edge_color = "light grey"
                        if node == current_node and neighbor == neighbor_list:
                            edge_color = "light green"

                    # Kanten ausgegraut
                    if step["step_type"] == "Priority Queue Empty":
                        edge_color = "light grey"

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
                        self.draw_bidirectional_edge(x1_no_node_clip, y1_no_node_clip, x2_no_node_clip,
                                                     y2_no_node_clip,
                                                     dx, dy, distance, middle_space, node, neighbor, weight,
                                                     visited_edges, current_node, neighbor_list, already_drawn_edges)
                    else:
                        self.draw_directed_edge(x1_no_node_clip, y1_no_node_clip, x2_no_node_clip, y2_no_node_clip,
                                                dx, dy, distance, middle_space, edge_color, weight,
                                                already_drawn_edges,
                                                node, neighbor)

    def draw_directed_edge(self, x1, y1, x2, y2, dx, dy, distance, middle_space, edge_color, weight,
                           already_drawn_edges, node, neighbor):
        weight_text = str(weight)
        text_width = len(weight_text) * 8

        middle_space += text_width / distance * 1.5

        segment_dx = dx / distance * middle_space * distance
        segment_dy = dy / distance * middle_space * distance

        middle_x = (x1 + x2) / 2
        middle_y = (y1 + y2) / 2

        available_space = distance * middle_space
        if text_width > available_space:
            extra_space = (text_width - available_space) / 2
            middle_x -= extra_space

        self.gui_frame.canvas.create_line(x1, y1, middle_x - segment_dx / 2, middle_y - segment_dy / 2,
                                          width=4, tags="edge", fill=edge_color, smooth=True, splinesteps=500)
        self.gui_frame.canvas.create_line(middle_x + segment_dx / 2, middle_y + segment_dy / 2, x2, y2,
                                          width=4, tags="edge", arrow="last", arrowshape=(10, 12, 5),
                                          fill=edge_color, smooth=True, splinesteps=500)
        self.gui_frame.canvas.create_text(middle_x, middle_y, text=weight_text, fill="black", font=("Arial", 14),
                                          tags="weight")
        already_drawn_edges.add((node, neighbor))

    def draw_bidirectional_edge(self, x1, y1, x2, y2, dx, dy, distance, middle_space, node, neighbor, weight,
                                visited_edges, current_node, neighbor_list, already_drawn_edges):
        forward_colour = "black"
        reverse_colour = "black"
        step = {}
        if self.parent.current_step != -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]


        # change edge color depending on state
        if step:
            if step["step_type"] == "Algorithm Finished":
                color = "light blue"
            if step["step_type"] == "Pick Node":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Initialize Node Distance":
                color = "light grey"
                if node == current_node:
                    color = "green"
            if step["step_type"] == "Set Start Node Distance":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Push Start Node to Priority Queue":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Heap Pop":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Visit Node":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Compare Distance":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Highlight Edge":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Begin Outer Loop":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Begin Inner Loop":

                if (node, neighbor) in visited_edges and node == current_node:
                    edge_color = "light green"
                elif node == current_node:
                    edge_color = "red"
                else:
                    edge_color = "light grey"
            if step["step_type"] == "Update Distance and Push to Heap":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Skip Visited Node":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Skip Visited Neighbor":
                color = "light grey"
                if node == current_node:
                    color = "yellow"
            if step["step_type"] == "Priority Queue Empty":
                color = "light grey"
                if node == current_node:
                    color = "yellow"

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

        # Forward edge
        x1_offset = x1 + perp_dx
        y1_offset = y1 + perp_dy
        x2_offset = x2 + perp_dx
        y2_offset = y2 + perp_dy
        middle_x_forward = (x1_offset + x2_offset) / 2 + segment_dx_expanded / 2
        middle_y_forward = (y1_offset + y2_offset) / 2 + segment_dy_expanded / 2

        self.gui_frame.canvas.create_line(x1_offset, y1_offset, middle_x_forward - segment_dx_expanded / 2,
                                          middle_y_forward - segment_dy_expanded / 2,
                                          width=4, tags="edge", fill=forward_colour, smooth=True, splinesteps=500)
        self.gui_frame.canvas.create_line(middle_x_forward + segment_dx_expanded / 2,
                                          middle_y_forward + segment_dy_expanded / 2,
                                          x2_offset, y2_offset, width=4, tags="edge", arrow="last",
                                          arrowshape=(10, 12, 5), fill=forward_colour, smooth=True, splinesteps=500)
        self.gui_frame.canvas.create_text(middle_x_forward, middle_y_forward, text=weight_text_forward, fill="black",
                                          font=("Arial", 13), tags="weight")

        # Reverse edge
        x1_offset = x1 - perp_dx
        y1_offset = y1 - perp_dy
        x2_offset = x2 - perp_dx
        y2_offset = y2 - perp_dy
        middle_x_reverse = (x1_offset + x2_offset) / 2 - segment_dx_expanded / 2
        middle_y_reverse = (y1_offset + y2_offset) / 2 - segment_dy_expanded / 2

        self.gui_frame.canvas.create_line(x2_offset, y2_offset, middle_x_reverse + segment_dx_expanded / 2,
                                          middle_y_reverse + segment_dy_expanded / 2,
                                          width=4, tags="edge", fill=reverse_colour, smooth=True, splinesteps=500)
        self.gui_frame.canvas.create_line(middle_x_reverse - segment_dx_expanded / 2,
                                          middle_y_reverse - segment_dy_expanded / 2,
                                          x1_offset, y1_offset, width=4, tags="edge", arrow="last",
                                          arrowshape=(10, 12, 5), fill=reverse_colour, smooth=True, splinesteps=500)
        self.gui_frame.canvas.create_text(middle_x_reverse, middle_y_reverse, text=weight_text_reverse,
                                          font=("Arial", 13),
                                          tags="weight")

        already_drawn_edges.add((node, neighbor))
        already_drawn_edges.add((neighbor, node))

    def get_distanze_text(self, step):
        return 0