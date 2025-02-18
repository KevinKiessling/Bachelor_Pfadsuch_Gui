import json
from tkinter import *
from tkinter import messagebox
from gui.Canvas_Frame import *
from gui.Pseudocode_Frame import *
from algorithms.dijkstra_list import *
from algorithms.dijkstra_Priority_queue_lazy import *
from algorithms.dijkstra_Priority_queue import *

import math
class Graph_Visualizer_Path:
    def __init__(self, gui_frame, node_positions, graph, start_node, parent):
        self.gui_frame = gui_frame
        self.node_positions = node_positions
        self.graph = graph
        self.parent = parent

        self.start_node = start_node
        self.path = {}

    def draw_path(self, path):
        self.gui_frame.canvas.delete("all")
        node_radius = self.parent.node_rad
        font_size = self.parent.font_size_node_label
        self.path = path.copy()
        already_drawn_edges = set()
        color = "lightblue"
        step = {}
        if self.parent.current_step != -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]
            print(step)

            distances = step["distances"]
        else:
            self.parent.update_gui()
            return

        discovered_node_true_color = self.parent.color_discovered_true
        discovered_node_false_color = self.parent.color_discovered_false
        current_node_color = self.parent.color_default
        d_v_color = self.parent.color_d_v
        start_node = None
        target_node = None

        if path:
            start_node = path[0][0]
            target_node = path[-1][1]
        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            dis_color = "grey"
            if step:
                if any(node in edge for edge in self.path):
                    color = self.parent.color_shortest_path
                    dis_color = "black"
                else:
                    color = "light grey"

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

        # Draw edges
        for node, edges in self.graph.items():
            for neighbor, weight in edges.items():
                if (node, neighbor) in already_drawn_edges:
                    continue

                edge_color = "light grey"
                if (node, neighbor) in path:
                    edge_color = self.parent.color_shortest_path


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
        step = {}
        if self.parent.current_step != -1:
            step = self.parent.steps_finished_algorithm[self.parent.current_step]
        weight_color = "light grey"  # Default weight color

        if step:
            if (node, neighbor) in self.path:
                weight_color = self.parent.color_shortest_path

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