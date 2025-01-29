

class Dijkstra_List():
    def __init__(self):
        super().__init__()
        self.steps = []
        self.shortest_path_edges = {}

    def run_dijkstra_list(self, graph, startnode):
        distances = {}


        L = list()
        prev_nodes = {}
        path_edges = {startnode: []}
        visited = {}
        visited_edges = set()
        #line 2
        for node in graph:
            visited[node] = None
            self.save_state(
                step_type="Pick Node_1",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List"
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
                current_list=L,
                selected_algorithm="Dijkstra_List"
            )
        #line 3
        for node in graph:
            self.save_state(
                step_type="Pick Node_2",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List"
            )

            distances[node] = float('inf')  # Set visited status to False for each node
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
                current_list=L,
                selected_algorithm="Dijkstra_List"
            )
        #line 4, 1
        distances[startnode] = 0
        self.save_state(
            step_type="Set Start Node Distance",
            current_node=startnode,
            current_distance=None,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited,
            visited_edges=visited_edges,
            current_list=L,
            selected_algorithm="Dijkstra_List"
        )
        #line 4,2
        self.save_state(
            step_type="Initialize List",
            current_node=startnode,
            current_distance=None,
            neighbor=None,
            edge_weight=None,
            distances=distances,
            prev_nodes=prev_nodes,
            visited=visited,
            visited_edges=visited_edges,
            current_list=L,
            selected_algorithm="Dijkstra_List"
        )
        for node in graph:
            self.save_state(
                step_type="Pick Node_3",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List"
            )
            L.append(node)
            self.save_state(
                step_type="Add Node to List",
                current_node=node,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List"
            )


        while L:
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
                current_list=L,
                selected_algorithm="Dijkstra_List"
            )
            u = min(L, key=lambda node: distances[node])
            self.save_state(
                step_type="Find Min in List",
                current_node=u,
                current_distance=distances[u],
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited.copy(),
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List",
            )
            L.remove(u)
            self.save_state(
                step_type="Remove min from List",
                current_node=u,
                current_distance=distances[u],
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited.copy(),
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List",
            )
            current_distance, current_node = distances[u], u
            print(u)
            visited[u] = True

            self.save_state(
                step_type="Visit Node u ",
                current_node=current_node,
                current_distance=current_distance,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited.copy(),
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List",
            )

            for neighbor, edge_weight in graph[u].items():
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
                    current_list=L,
                    selected_algorithm="Dijkstra_List"
                )
                if visited[neighbor]:
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
                        current_list=L,
                        selected_algorithm="Dijkstra_List"
                    )
                    continue
                visited_edges.add((current_node, neighbor))

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
                    current_list=L,
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
                    current_list=L,
                    selected_algorithm="Dijkstra_List",
                )
        if not L:
            self.save_state(
                step_type="List Empty",
                current_node=None,
                current_distance=None,
                neighbor=None,
                edge_weight=None,
                distances=distances,
                prev_nodes=prev_nodes,
                visited=visited,
                visited_edges=visited_edges,
                current_list=L,
                selected_algorithm="Dijkstra_List"
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
            current_list=L,
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
        current_list,
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
            "list": current_list.copy(),
        }
        self.steps.append(state)

        # print steps, debug
    def print_step(self):
        print(self.steps)

