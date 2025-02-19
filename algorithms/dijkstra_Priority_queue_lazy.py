import heapq


class Dijkstra_Priority_Queue_Lazy():
    def __init__(self):
        super().__init__()
        self.steps = []
        self.shortest_path_edges = {}


    #dijkstra algorithmus mit priority Queue
    def run_dijkstra_priority_queue_lazy(self, graph, startnode):
        distances = {}
        priority_queue = []
        prev_nodes = {}
        path_edges = {}
        visited = {}  # Initialize as empty; will populate in the loop
        visited_edges = set()

        for node in graph:
            visited[node] = None
            self.save_state(
                step_type="Pick Node",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )

            visited[node] = False  # Set visited status to False for each node
            self.save_state(
                step_type="Initialize Visited",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )
            distances[node] = float('inf')
            self.save_state(
                step_type="Initialize Node Distance",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )

        distances[startnode] = 0
        path_edges[startnode] = []

        self.save_state(
            step_type="Set Start Node Distance",
            current_node=startnode,
            current_distance=0,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited,
            visited_edges=visited_edges,
            priority_queue=priority_queue,
            selected_algorithm="Dijkstra_PQ_lazy"
        )

        heapq.heappush(priority_queue, (0, startnode))

        self.save_state(
            step_type="Push Start Node to Priority Queue",
            current_node=startnode,
            current_distance=0,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited,
            visited_edges=visited_edges,
            priority_queue=priority_queue,
            selected_algorithm="Dijkstra_PQ_lazy"
        )

        while priority_queue:
            self.save_state(
                step_type="Begin Outer Loop",
                current_node=None,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )
            current_distance, current_node = heapq.heappop(priority_queue)
            self.save_state(
                step_type="Heap Pop",
                current_node=current_node,
                current_distance=current_distance,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )
            self.save_state(
                step_type="Check if visited",
                current_node=current_node,
                current_distance=current_distance,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )
            if visited[current_node]:
                self.save_state(
                    step_type="Skip Visited Node",
                    current_node=current_node,
                    current_distance=current_distance,
                    neighbor=None,
                    edge_weight=None,
                    distances=distances,
                    prev_nodes=prev_nodes,
                    visited=visited,
                    visited_edges=visited_edges,
                    priority_queue=priority_queue,
                    selected_algorithm="Dijkstra_PQ_lazy"
                )
                continue

            visited[current_node] = True  # Mark the node as visited
            self.save_state(
                step_type="Visit Node",
                current_node=current_node,
                current_distance=current_distance,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
            )

            for neighbor, edge_weight in graph[current_node].items():
                self.save_state(
                    step_type="Begin Inner Loop",
                    current_node=current_node,
                    current_distance=current_distance,
                    neighbor=neighbor,
                    edge_weight=edge_weight,
                    distances=distances,
                    prev_nodes=prev_nodes,
                    visited=visited,
                    visited_edges=visited_edges,
                    priority_queue=priority_queue,
                    selected_algorithm="Dijkstra_PQ_lazy"
                )
                if visited[neighbor]:

                    visited_edges.add((current_node, neighbor))

                    self.save_state(
                        step_type="Skip Visited Neighbor",
                        current_node=current_node,
                        current_distance=current_distance,
                        neighbor=neighbor,
                        edge_weight=edge_weight,
                        distances=distances,
                        prev_nodes=prev_nodes,
                        visited=visited,
                        visited_edges=visited_edges,
                        priority_queue=priority_queue,
                        selected_algorithm="Dijkstra_PQ_lazy"
                    )
                    continue
                visited_edges.add((current_node, neighbor))
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
                    priority_queue=priority_queue,
                    selected_algorithm="Dijkstra_PQ_lazy"
                )
                new_distance = current_distance + edge_weight

                self.save_state(
                    step_type="Compare Distance",
                    current_node=current_node,
                    current_distance=current_distance,
                    neighbor=neighbor,
                    edge_weight=edge_weight,
                    distances=distances,
                    prev_nodes=prev_nodes,
                    visited=visited,
                    visited_edges=visited_edges,
                    priority_queue=priority_queue,
                    selected_algorithm="Dijkstra_PQ_lazy"
                )

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    path_edges[neighbor] = path_edges[current_node] + [(current_node, neighbor)]
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
                        priority_queue=priority_queue,
                        selected_algorithm="Dijkstra_PQ_lazy"
                    )
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    self.save_state(
                        step_type="Push to Heap",
                        current_node=current_node,
                        current_distance=current_distance,
                        neighbor=neighbor,
                        edge_weight=edge_weight,
                        distances=distances,
                        prev_nodes=prev_nodes,
                        visited=visited,
                        visited_edges=visited_edges,
                        priority_queue=priority_queue,
                        selected_algorithm="Dijkstra_PQ_lazy"
                    )
        if not priority_queue:
            self.save_state(
                step_type="Priority Queue Empty",
                current_node=None,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                priority_queue=priority_queue,
                selected_algorithm="Dijkstra_PQ_lazy"
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
            priority_queue=priority_queue,
            selected_algorithm="Dijkstra_PQ_lazy"
        )

        self.shortest_path_edges = path_edges
        return self.steps, self.shortest_path_edges

    #Speichert Schritt des Algorithmus
    def save_state(self, step_type, current_node, current_distance, neighbor, edge_weight, distances, prev_nodes,
                   visited, visited_edges, priority_queue, selected_algorithm):
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


    #print steps, debug
    def print_step(self):
        for step in self.steps:
            print(step["step_type"])

