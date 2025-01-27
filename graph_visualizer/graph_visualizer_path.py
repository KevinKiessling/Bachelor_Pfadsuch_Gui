import json
from tkinter import *
from tkinter import messagebox
from gui.frame import *
from gui.pseudocode_frame import *
from algorithmen.dijkstra_list import *
from algorithmen.dijkstra_Priority_queue_lazy import *
from algorithmen.dijkstra_Priority_queue import *

import math
class Graph_Visualizer_Path:
    def __init__(self, gui_frame, node_positions, graph,selected_nodes, start_node, parent):
        self.gui_frame = gui_frame
        self.node_positions = node_positions
        self.graph = graph
        self.parent = parent
        self.selected_nodes = selected_nodes
        self.start_node = start_node
    def draw_path(self, path):
        self.gui_frame.canvas.delete("all")
        node_radius = 30
        font_size = 16
        already_drawn_edges = set()
        distances = self.parent.steps_finished_algorithm[-1]["distances"]
        start_node = None
        target_node = None

        if path:
            start_node = path[0][0]
            target_node = path[-1][1]

        for node, (x, y) in self.parent.node_positions.items():
            if node == start_node:
                color = self.parent.path_color
            elif node == target_node:
                color = self.parent.path_color
            else:
                color = "light grey"

            if self.parent.steps_finished_algorithm:

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

            if node in self.parent.selected_nodes:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                                  fill="green")

                self.gui_frame.canvas.create_text(
                    x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                )
                if node == self.parent.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(
                        x, y, text=display_text, fill="black", font=("Arial", font_size), anchor="center"
                    )
            else:
                self.gui_frame.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                                  fill=color)

                if node == self.parent.start_node:
                    self.gui_frame.canvas.create_text(x, y, text="Start", fill="black", font=("Arial", font_size))
                else:
                    self.gui_frame.canvas.create_text(x, y, text=display_text, fill="black", font=("Arial", font_size))

        # Zeichne alle Kanten, dabei wird zwischen 2 Varianten unterschieden, Direkt oder Bidirekt
        for node, edges in self.parent.graph.items():
            for neighbor, weight in edges.items():

                if (node, neighbor) in already_drawn_edges or (neighbor, node) in already_drawn_edges:
                    continue

                edge_color = "light grey"

                if (node, neighbor) in path:
                    edge_color = self.parent.path_color

                if neighbor in self.parent.node_positions:

                    x1, y1 = self.parent.node_positions[node]
                    x2, y2 = self.parent.node_positions[neighbor]

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
                            forward_colour = self.parent.path_color
                        if (neighbor, node) in path:
                            reverse_colour = self.parent.path_color

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