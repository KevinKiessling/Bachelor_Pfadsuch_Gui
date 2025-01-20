

class Dijkstra_List():
    def __init__(self):
        super().__init__()
        self.steps = []
        self.shortest_path_edges = {}

    def run_dijkstra_list(self, graph, startnode):
        distances = {node: float("inf") for node in graph}
        distances[startnode] = 0
        L = list(graph.keys())
        prev_nodes = {}
        path_edges = {startnode: []}
        visited = set()
        visited_edges = set()

        def convert_to_priority_queue(L, distances):

            return sorted([(distances[node], node) for node in L], key=lambda x: x[0])

        self.save_state(
            step_type="Initialization",
            current_node=None,
            current_distance=None,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited.copy(),
            visited_edges=visited_edges,
            priority_queue=convert_to_priority_queue(L, distances),
            selected_algorithm="Dijkstra_List",
        )

        while L:
            u = min(L, key=lambda node: distances[node])
            L.remove(u)

            visited.add(u)

            self.save_state(
                step_type="Select Node",
                current_node=u,
                current_distance=distances[u],
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited.copy(),
                visited_edges=visited_edges,
                priority_queue=convert_to_priority_queue(L, distances),
                selected_algorithm="Dijkstra_List",
            )
            if distances[u] == float("inf"):
                continue

            # Step 10: Explore neighbors of u
            for neighbor, edge_weight in graph[u].items():
                if neighbor in visited:
                    continue
                visited_edges.add((u, neighbor))

                self.save_state(
                    step_type="Highlight Edge",
                    current_node=u,
                    current_distance=distances[u],
                    neighbor=neighbor,
                    edge_weight=edge_weight,
                    distances=distances,
                    prev_nodes=prev_nodes,
                    visited=visited.copy(),
                    visited_edges=visited_edges,
                    priority_queue=convert_to_priority_queue(L, distances),
                    selected_algorithm="Dijkstra_List",
                )

                new_distance = distances[u] + edge_weight




                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    path_edges[neighbor] = path_edges[u] + [(u, neighbor)]
                    prev_nodes[neighbor] = u

                    self.save_state(
                        step_type="Update Distance",
                        current_node=u,
                        current_distance=distances[u],
                        neighbor=neighbor,
                        edge_weight=edge_weight,
                        distances=distances,
                        prev_nodes=prev_nodes,
                        visited=visited.copy(),
                        visited_edges=visited_edges,
                        priority_queue=convert_to_priority_queue(L, distances),
                        selected_algorithm="Dijkstra_List",
                    )

        self.save_state(
            step_type="Algorithm Finished",
            current_node=None,
            current_distance=None,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited.copy(),
            visited_edges=visited_edges,
            priority_queue=convert_to_priority_queue(L, distances),
            selected_algorithm="Dijkstra_List",
        )

        self.shortest_path_edges = path_edges
        return self.steps, self.shortest_path_edges

    def save_state(
        self,
        step_type,
        current_node,
        current_distance,
        neighbor,
        edge_weight,
        distances,
        prev_nodes,
        visited,
        visited_edges,
        priority_queue,
        selected_algorithm,
    ):
        state = {
            "selected_algorithm": selected_algorithm,
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

        # print steps, debug
    def print_step(self):
        print(self.steps)

