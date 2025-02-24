import networkx as nx
from algorithms.dijkstra_list import *
from algorithms.dijkstra_Priority_queue_lazy import *
from algorithms.dijkstra_Priority_queue import *

class DijkstraTester:
    def __init__(self, graph, start_node, selected_algorithm):
        self.graph = graph
        self.start_node = start_node
        self.selected_algorithm = selected_algorithm
        self.steps_finished_algorithm = []
        self.shortest_paths = {}

    def run_dijkstra_implementation(self):

        if self.start_node not in self.graph:
            print(f"Warning: Start node {self.start_node} is not in the graph. Skipping test.")
            return

        if self.selected_algorithm == "Dijkstra_PQ_Lazy":
            self.dijkstra_pq_lazy = Dijkstra_Priority_Queue_Lazy()
            self.steps_finished_algorithm, self.shortest_paths = self.dijkstra_pq_lazy.run_dijkstra_priority_queue_lazy(
                self.graph, self.start_node)

        elif self.selected_algorithm == "Dijkstra_PQ":
            self.dijkstra_pq = Dijkstra_Priority_Queue()
            self.steps_finished_algorithm, self.shortest_paths = self.dijkstra_pq.run_dijkstra_priority_queue(
                self.graph, self.start_node)

        elif self.selected_algorithm == "Dijkstra_List":
            self.dijkstra_list = Dijkstra_List()
            self.steps_finished_algorithm, self.shortest_paths = self.dijkstra_list.run_dijkstra_list(self.graph,
                                                                                                      self.start_node)

    def test_dijkstra_algorithm(self, source_node):
        graph_data = self.graph
        G = nx.DiGraph()
        if source_node not in self.graph:
            print(f"Warning: Source node {source_node} is not in the graph. Skipping test.")
            return False
        for node, neighbors in graph_data.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        print(f"Graph nodes: {list(G.nodes)}")
        print(f"Graph edges: {list(G.edges(data=True))}")
        print(f"Source node: {source_node}")

        if source_node not in G:
            print(f"Error: Source node {source_node} is not in the graph.")
            return False

        computed_distances_nx = nx.single_source_dijkstra_path_length(G, source_node)
        computed_distances_step = self.steps_finished_algorithm[-1]["distances"]

        print("NetworkX computed distances:", computed_distances_nx)
        print("Algorithm computed distances:", computed_distances_step)

        all_nodes = set(computed_distances_nx.keys()).union(set(computed_distances_step.keys()))
        for node in all_nodes:
            expected_distance = computed_distances_nx.get(node, float('inf'))
            computed_distance_step = computed_distances_step.get(node, float('inf'))

            if computed_distance_step != expected_distance:
                print(f"Test failed for node {node}: expected {expected_distance}, got {computed_distance_step}")
                return False

        print("All tests passed.")
        return True

    def test_edge_cases(self):

        edge_cases = [
            {'A': {}},
            {'A': {}, 'B': {}},
            {'A': {'B': -1}, 'B': {}},
            {'A': {'B': 1}, 'B': {'C': 2}, 'C': {'A': 3}},
            {'A': {'B': 1, 'C': 4}, 'B': {'C': 2}, 'C': {}},
            {chr(65 + i): {chr(66 + i): 1} for i in range(100)} | {chr(65 + 99): {}}
        ]

        for case in edge_cases:
            self.graph = case
            self.run_dijkstra_implementation()
            if not self.test_dijkstra_algorithm(self.start_node):
                print(f"Test failed for graph: {case}")
                return False

        print("All edge case tests passed.")
        return True

# Example Usage
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}
start_node = 'A '
selected_algorithm = "Dijkstra_List"

tester = DijkstraTester(graph, start_node, selected_algorithm)
tester.run_dijkstra_implementation()
tester.test_dijkstra_algorithm(start_node)
tester.test_edge_cases()