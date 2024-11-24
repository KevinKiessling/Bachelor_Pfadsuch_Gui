import heapq


class Dijkstra_Priority_Queue():
    def __init__(self):
        super().__init__()
        self.steps = []


    #dijkstra algorithmus mit priority Queue
    def run_dijkstra_list(self, graph, startnode):


        distances = {node: float('inf') for node in graph}
        distances[startnode] = 0
        node_in_queue = {startnode: 0}

        priority_queue = [(0, startnode)]
        prev_nodes = {}
        visited = set()
        visited_edges = set()
        self.save_state(
            step_type="Initialization",
            current_node=None,
            current_distance=None,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited,
            visited_edges=visited_edges,
            priority_queue=priority_queue
        )

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node in visited:
                continue

            visited.add(current_node)
            node_in_queue.pop(current_node, None)

            self.save_state(
                step_type="Select Node",
                current_node=current_node,
                current_distance=current_distance,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue
            )

            for neighbor, edge_weight in graph[current_node].items():
                if neighbor in visited:
                    continue
                new_distance = current_distance + edge_weight
                self.save_state(
                    step_type="Highlight Edge",
                    current_node=current_node,
                    current_distance=current_distance,
                    neighbor=neighbor,
                    edge_weight=edge_weight,
                    distances=distances,
                    prev_nodes=prev_nodes,
                    visited=visited,
                    visited_edges=visited_edges,
                    priority_queue=priority_queue
                )
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

                    if neighbor not in node_in_queue or new_distance < node_in_queue[neighbor]:
                        heapq.heappush(priority_queue, (new_distance, neighbor))
                        node_in_queue[neighbor] = new_distance  # Update tracking
                        visited_edges.add((current_node, neighbor))
                        self.save_state(
                            step_type="Update Distance",
                            current_node=current_node,
                            current_distance=current_distance,
                            neighbor=neighbor,
                            edge_weight=edge_weight,
                            distances=distances,
                            prev_nodes=prev_nodes,
                            visited=visited,
                            visited_edges=visited_edges,
                            priority_queue=priority_queue
                        )

        self.save_state(
            step_type="Algorithm Finished",
            current_node=None,
            current_distance=None,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited,
            visited_edges=visited_edges,
            priority_queue=priority_queue
        )
        return self.steps

    def save_state(self, step_type, current_node, current_distance, neighbor, edge_weight, distances, prev_nodes,
                   visited, visited_edges, priority_queue):
        """Save the current step's state for replay in the GUI."""
        state = {
            "step_type": step_type,
            "current_node": current_node,
            "current_distance": current_distance,
            "neighbor": neighbor,
            "edge_weight": edge_weight,
            "distances": distances.copy(),
            "prev_nodes": prev_nodes.copy(),
            "visited": visited.copy(),
            "visited_edges": visited_edges.copy(),
            "priority_queue": priority_queue[:],
        }
        self.steps.append(state)


    #print steps, debug
    def print_step(self):
        print(self.steps)