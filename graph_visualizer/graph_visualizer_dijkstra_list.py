import json
from tkinter import *
from tkinter import messagebox
from gui.Canvas_Frame import *
from gui.Pseudocode_Frame import *
from algorithms.dijkstra_list import *
from algorithms.dijkstra_Priority_queue_lazy import *
from algorithms.dijkstra_Priority_queue import *

import math

class Graph_Visualizer_Dijkstra_List:
    """
    Klassen zum zeichnen der Graphen während des Dijkstra-List Algorithmus
    """
    def __init__(self, gui_frame, node_positions, graph, start_node, parent):
        self.gui_frame = gui_frame
        self.node_positions = node_positions
        self.graph = graph
        self.parent = parent
        self.start_node = start_node



    def draw_graph_dijkstra_list(self, current_node, neighbor_list, distances, visited, visited_edges):
        """
        Zeichnet den Graphen
        :param current_node: aktueller Knoten
        :param neighbor_list: Nachbarknoten vom aktuellen Knoten
        :param distances: Distanceliste
        :param visited: Besuchte Knoten
        :param visited_edges: Besuchete Kanten
        :return:
        """
        self.gui_frame.canvas.delete("all")
        node_radius = self.parent.node_rad
        font_size = self.parent.font_size_node_label
        already_drawn_edges = set()
        color = "lightblue"
        step = {}
        if self.parent.current_step != -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]
            print(step)
        discovered_node_true_color = self.parent.color_discovered_true
        discovered_node_false_color = self.parent.color_discovered_false
        current_node_color = self.parent.color_default
        d_v_color = self.parent.color_d_v
        dis_color = "black"
        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            # color nodes based on steptype
            if step:
                # wenn alg. durchgelaufen, dann sind alle Knoten hellblau
                if step["step_type"] == "Algorithm Finished":
                    color = "light blue"
                if step["step_type"] == "Initialize List":
                    color = "light grey"
                    dis_color = "grey"
                # wenn Knoten während initialisierung gewählt wird, dann ist dieser Knoten gelb. Rest ist grau
                if step["step_type"] == "Pick Node":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color
                if step["step_type"] == "Pick Node_1":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color
                if step["step_type"] == "Pick Node_2":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color
                if step["step_type"] == "Pick Node_3":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color
                if step["step_type"] == "Add Node to List":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        color = self.parent.color_heap
                        dis_color = "black"
                #  NEEDS WORK!! Aktueller Knoten gelb, sonst grau
                if step["step_type"] == "Initialize Node Distance":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color
                # StartKnoten gelb, rest grau
                if step["step_type"] == "Set Start Node Distance":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color
                # StartKnoten wird auf PQ pushed, also alles grau ausser startKnoten
                if step["step_type"] == "Push Start Node to Priority Queue":
                    color = "light grey"
                    if node == current_node:
                        color = self.parent.color_heap
                if step["step_type"] == "Find Min in List":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = self.parent.color_heap
                if step["step_type"] == "Remove min from List":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color


                # NEEDS WORK!! Füge current node den Discoverten Nodes hinzu, visited nodes = grün, aktueller = #4bf569, rest grau
                if step["step_type"] == "Visit Node":
                    '''color = "light grey"
                    if visited[node]:
                        color = discovered_node_true_color
                    if node == current_node:
                        color = discovered_node_true_color
                    if not visited[node]:
                        color = discovered_node_false_color'''
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        if visited.get(current_node):
                            # print(visited.get(current_node))
                            color = discovered_node_true_color
                        elif not visited.get(current_node):
                            color = discovered_node_false_color
                if step["step_type"] == "Visit Node u ":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        if visited.get(current_node):
                            # print(visited.get(current_node))
                            color = discovered_node_true_color
                        elif not visited.get(current_node):
                            color = discovered_node_false_color

                # initial visit, orange for false
                if step["step_type"] == "Initialize Visited":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                    # das If crashed niemals, da .get safe ist.
                    if visited.get(node) is None:
                        color = "light grey"
                    elif visited[node]:
                        color = discovered_node_true_color
                    else:
                        color = discovered_node_false_color

                # NEEDS WORK!! vergleiche Distanzen also alles bis auf Current node und aktueller nachbar gray, die beiden sind gelb
                if step["step_type"] == "Compare Distance":
                    color = "light grey"
                    if node == current_node:
                        color = current_node_color  # d[u]
                    if node in neighbor_list:
                        color = d_v_color  # d[v]

                # Aktueller Knoten gelb, rest grau.
                if step["step_type"] == "Highlight Edge":
                    color = "light grey"
                    dis_color = "grey"
                    # if visited[node]:
                    # color = discovered_node_true_color
                    if node == current_node:
                        color = current_node_color
                        dis_color = "black"
                    # if not visited[node]:
                    # color = discovered_node_false_color
                    if node in neighbor_list:
                        dis_color = "black"
                        color = discovered_node_false_color

                # Färbe Knoten die in Queue sind #57b3ea, rest grau
                if step["step_type"] == "Begin Outer Loop":
                    color = "light grey"
                    dis_color = "grey"
                # if any(n == node for _, n in step["priority_queue"]):
                # color = "#57b3ea"

                # Aktueller Knoten gelb, rest grau, hier werden nur alle Kanten highlighted
                if step["step_type"] == "Begin Inner Loop":
                    color = "light grey"
                    dis_color = "grey"
                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color

                # Update Distanzen von Nachbar, yellow für knoten der updated wird, rest grau
                if step["step_type"] == "Update Distance":
                    color = "light grey"
                    dis_color = "grey"

                    if node == current_node:
                        dis_color = "black"
                        color = current_node_color  # d[u]
                    if node in neighbor_list:
                        dis_color = "black"
                        color = d_v_color  # d[v]


                # Überspringe besuchte Nachbarn
                if step["step_type"] == "Skip Visited Neighbor":
                    color = "light grey"
                    dis_color = "grey"
                    # if visited[node]:
                    # color = discovered_node_true_color
                    if node == current_node:
                        color = "yellow"
                        dis_color = "black"
                    # if not visited[node]:
                    # color = discovered_node_false_color
                    if node in neighbor_list:
                        dis_color = "black"
                        color = discovered_node_true_color


            # Knoten werte
            distance_text = distances.get(node, None)
            if distance_text is None:
                distance_text = "--"
            elif distance_text == float('inf'):
                distance_text = "∞"
            else:
                distance_text = f"{distance_text}"

            self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                              fill=color)

            if node == self.parent.start_node:
                if color == "yellow":
                    self.gui_frame.canvas.create_oval(
                        x - node_radius - 5, y - node_radius - 5, x + node_radius + 5, y + node_radius + 5,
                        outline="light grey",
                        width=3,
                        dash=(3, 3)  # Dashed line pattern
                    )
                else:
                    self.gui_frame.canvas.create_oval(
                        x - node_radius - 5, y - node_radius - 5, x + node_radius + 5, y + node_radius + 5,
                        outline=color,
                        width=3,
                        dash=(3, 3)  # Dashed line pattern
                    )

            distance_font_size = max(font_size - 2, 1)
            if len(distance_text) >= 5:
                distance_font_size = max(distance_font_size - (len(distance_text) - 4) * 2, 1)

            if self.parent.show_distance_on_nodes:

                vertical_offset = node_radius * 0.4
                self.gui_frame.canvas.create_text(
                    x, y - vertical_offset,
                    text=node,
                    fill=dis_color,
                    font=("Arial", font_size, "bold"),
                    anchor="center"
                )

                self.gui_frame.canvas.create_text(
                    x, y + vertical_offset,
                    text=distance_text,
                    fill=dis_color,
                    font=("Arial", distance_font_size),
                    anchor="center"
                )
            else:
                self.gui_frame.canvas.create_text(
                    x, y,
                    text=node,
                    fill=dis_color,
                    font=("Arial", font_size, "bold"),
                    anchor="center"
                )

        # Draw edges
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():
                if (node, neighbor) in already_drawn_edges:
                    continue

                edge_color = "black"
                if step:
                    if step["step_type"] == "Algorithm Finished":
                        edge_color = "black"
                    elif step["step_type"] in {
                        "Pick Node", "Initialize Node Distance", "Initialize Visited",
                        "Set Start Node Distance", "Push Start Node to Priority Queue",
                        "Heap Pop", "Visit Node", "Begin Outer Loop",
                        "Push to Heap", "Skip Visited Node", "Priority Queue Empty", "Check if visited","Pick Node_1","Pick Node_2","Pick Node_3",
                        "Initialize List", "Add Node to List", "Find Min in List", "Remove min from List", "Visit Node u "
                    }:
                        edge_color = "light grey"
                    elif step["step_type"] == "Compare Distance":
                        edge_color = "light grey"
                        if node == current_node and neighbor in neighbor_list:
                            edge_color = self.parent.color_edge_highlight
                    elif step["step_type"] == "Update Distance":
                        edge_color = "light grey"
                        if node == current_node and neighbor in neighbor_list:
                            edge_color = self.parent.color_edge_highlight
                    elif step["step_type"] == "Highlight Edge":
                        edge_color = "light grey"
                        if node == current_node and neighbor in neighbor_list:
                            edge_color = self.parent.color_edge_highlight
                    elif step["step_type"] == "Begin Inner Loop":
                        if (node, neighbor) in visited_edges and node == current_node:
                            # visited edges
                            # edge_color = "light green"
                            edge_color = "light grey"
                        elif node == current_node:
                            edge_color = self.parent.color_edge_highlight
                        else:
                            edge_color = "light grey"
                    elif step["step_type"] == "Skip Visited Neighbor":
                        edge_color = "light grey"
                        if node == current_node and neighbor in neighbor_list:
                            edge_color = self.parent.color_edge_highlight
                    elif step["step_type"] == "Find Position in Heap":
                        edge_color = "light grey"
                    elif step["step_type"] == "Remove from Heap":
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
                    self.draw_directed_edge(
                        x1_no_node_clip, y1_no_node_clip, x2_no_node_clip, y2_no_node_clip,
                        dx, dy, distance, middle_space, edge_color, weight,
                        already_drawn_edges, node, neighbor
                    )

    def draw_directed_edge(self, x1, y1, x2, y2, dx, dy, distance, middle_space, edge_color, weight,
                           already_drawn_edges, node, neighbor):
        """
        Zeichnet eine Kante
        :param x1: x start
        :param y1: y start
        :param x2: x ziel
        :param y2: y ziel
        :param dx: x offset
        :param dy: y offset
        :param distance: Entfernung der Knoten
        :param middle_space: Mittelraum
        :param edge_color: Farbe
        :param weight: Gewicht
        :param already_drawn_edges: liste mit bereits gezeichneten Kanten
        :param node: Knoten
        :param neighbor: Nachbar
        :return:
        """
        step = {}
        if self.parent.current_step != -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]
        weight_color = "black"  # Default weight color

        if step:
            if step["step_type"] == "Algorithm Finished":
                weight_color = "black"
            elif step["step_type"] == "Pick Node":
                weight_color = "light grey"
            elif step["step_type"] == "Pick Node_1":
                weight_color = "light grey"
            elif step["step_type"] == "Pick Node_2":
                weight_color = "light grey"
            elif step["step_type"] == "Pick Node_3":
                weight_color = "light grey"
            elif step["step_type"] == "Initialize List":
                weight_color = "light grey"
            elif step["step_type"] == "Initialize Node Distance":
                weight_color = "light grey"
            elif step["step_type"] == "Set Start Node Distance":
                weight_color = "light grey"
            elif step["step_type"] == "Add Node to List":
                weight_color = "light grey"
            elif step["step_type"] == "Find Min in List":
                weight_color = "light grey"
            elif step["step_type"] == "Visit Node u ":
                weight_color = "light grey"
            elif step["step_type"] == "Remove min from List":
                weight_color = "light grey"
            elif step["step_type"] == "Initialize Visited":
                weight_color = "light grey"
            elif step["step_type"] == "Find Position in Heap":
                weight_color = "light grey"
            elif step["step_type"] == "Priority Queue Empty":
                weight_color = "light grey"
            elif step["step_type"] == "Push Start Node to Priority Queue":
                weight_color = "light grey"
            elif step["step_type"] == "Begin Outer Loop":
                weight_color = "light grey"
            elif step["step_type"] == "Skip Visited Node":
                weight_color = "light grey"
            elif step["step_type"] == "Heap Pop":
                weight_color = "light grey"

            # only current edges should do that

            elif step["step_type"] == "Highlight Edge":
                weight_color = "light grey"
                current_node = step.get("current_node")
                current_neighbor = step.get("neighbor")

                if current_node and current_neighbor and node == current_node and neighbor == current_neighbor:
                    weight_color = self.parent.color_edge_highlight

            elif step["step_type"] == "Visit Node":
                weight_color = "light grey"

            elif step["step_type"] == "Compare Distance":
                weight_color = "light grey"
                current_node = step.get("current_node")
                current_neighbor = step.get("neighbor")

                if current_node and current_neighbor:
                    if node == current_node and neighbor == current_neighbor:
                        weight_color = self.parent.color_edge_highlight
                    else:
                        weight_color = "light grey"

            elif step["step_type"] == "Push to Heap":
                weight_color = "light grey"
            elif step["step_type"] == "Remove from Heap":
                weight_color = "light grey"
            # only current edges should do that
            elif step["step_type"] == "Update Distance":
                weight_color = "light grey"
                current_node = step.get("current_node")
                current_neighbor = step.get("neighbor")

                if current_node and current_neighbor:
                    if node == current_node and neighbor == current_neighbor:
                        weight_color = self.parent.color_edge_highlight
                    else:
                        weight_color = "light grey"

            # alles gewichte -> grau, ausser ausgehender vom aktuellen Knoten. -> besucht grün, offen rot
            elif step["step_type"] == "Begin Inner Loop":
                current_node = step.get("current_node")
                visited_nb = step.get("visited_edges")
                if (node, neighbor) in visited_nb and node == current_node:
                    # visited edges
                    # weight_color = "light green"
                    weight_color = "light grey"
                elif node == current_node:
                    weight_color = self.parent.color_edge_highlight
                else:
                    weight_color = "light grey"
            elif step["step_type"] == "Skip Visited Neighbor":
                current_node = step.get("current_node")
                visited_nb = step.get("neighbor")
                weight_color = "light grey"
                if node == current_node and neighbor in visited_nb:

                    weight_color = self.parent.color_edge_highlight

            # Add any other step types with different weight colors as needed
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
        self.gui_frame.canvas.create_text(middle_x, middle_y, text=weight_text, fill=weight_color, font=("Arial", self.parent.font_size_edge_weight),
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
            if step["step_type"] == "Initialize Node Distance and Visited":
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

