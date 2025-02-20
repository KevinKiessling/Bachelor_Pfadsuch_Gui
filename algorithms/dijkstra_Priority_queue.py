import heapq

class Dijkstra_Priority_Queue:
    def __init__(self):
        super().__init__()
        self.steps = []
        self.shortest_path_edges = {}
    def run_dijkstra_priority_queue(self, graph, startnode):
        distances = {}
        visited = {}
        priority_queue = []
        prev_nodes = {}
        path_edges = {}
        visited_edges = set()

        # Initialize distances and discovered nodes
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

            visited[node] = False
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
        # Set distance for start node
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

            # Extract the node with the smallest distance
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
            visited[current_node] = True
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


            # Process all neighbors
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
                    self.save_state(
                        step_type="Find Position in Heap",
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
                    self.remove_from_priority_queue(priority_queue, neighbor)
                    self.save_state(
                        step_type="Remove from Heap",
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
                    prev_nodes[neighbor] = current_node
                    visited_edges.add((current_node, neighbor))

                    # Add the updated entry to the priority queue
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

    def remove_from_priority_queue(self, priority_queue, target_node):
        # Remove all occurrences of the target node from the priority queue
        priority_queue[:] = [(dist, node) for dist, node in priority_queue if node != target_node]

        # Manually restore the heap property without using heapq
        for i in range(len(priority_queue) // 2 - 1, -1, -1):
            self._sift_down(priority_queue, i)

        # Check if the resulting priority queue is still a valid min-heap
        if not self.is_valid_min_heap(priority_queue):
            print("The priority queue is not a valid min-heap after removal!")

    def _sift_down(self, priority_queue, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(priority_queue) and priority_queue[left][0] < priority_queue[smallest][0]:
            smallest = left
        if right < len(priority_queue) and priority_queue[right][0] < priority_queue[smallest][0]:
            smallest = right

        if smallest != index:
            priority_queue[index], priority_queue[smallest] = priority_queue[smallest], priority_queue[index]
            self._sift_down(priority_queue, smallest)

    def is_valid_min_heap(self, priority_queue):
        # Check if the priority queue is a valid min-heap
        n = len(priority_queue)
        for i in range(n // 2):  # Only need to check non-leaf nodes
            left = 2 * i + 1
            right = 2 * i + 2

            # Check if the left child is smaller than the parent
            if left < n and priority_queue[i][0] > priority_queue[left][0]:
                return False

            # Check if the right child is smaller than the parent
            if right < n and priority_queue[i][0] > priority_queue[right][0]:
                return False

        return True

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

    def print_steps(self):
        for step in self.steps:
            print(step["step_type"])
