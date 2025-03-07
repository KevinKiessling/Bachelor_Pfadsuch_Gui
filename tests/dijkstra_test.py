import networkx as nx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithms import *
from algorithms.dijkstra_list import *
from algorithms.dijkstra_Priority_queue_lazy import *
from algorithms.dijkstra_Priority_queue import *

class DijkstraTester:
    '''Programm um die Dijkstra-Algorithmen mit bekannt korrekten des NetworkX-Frameworks zu vergleichen'''
    def __init__(self, graph, start_node, selected_algorithm):
        self.graph = graph
        self.start_node = start_node
        self.selected_algorithm = selected_algorithm
        self.steps_finished_algorithm = []
        self.shortest_paths = {}

    def run_dijkstra_implementation(self):
        if self.start_node not in self.graph:
            print(f"Warnung: Startknoten {self.start_node} ist nicht im Graph. Test wird übersprungen.")
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
            print(f"Warnung: Startknoten {source_node} ist nicht im Graph. Test wird übersprungen.")
            return False
        for node, neighbors in graph_data.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        print(f"Graph Knoten: {list(G.nodes)}")
        print(f"Graph Kanten: {list(G.edges(data=True))}")
        print(f"Startknoten: {source_node}")

        if source_node not in G:
            print(f"Fehler: Startknoten {source_node} ist nicht im Graph.")
            return False

        computed_distances_nx = nx.single_source_dijkstra_path_length(G, source_node)
        computed_distances_step = self.steps_finished_algorithm[-1]["distances"]

        print("NetworkX berechnete Distanzen:", computed_distances_nx)
        print("Algorithmus berechnete Distanzen:", computed_distances_step)

        all_nodes = set(computed_distances_nx.keys()).union(set(computed_distances_step.keys()))
        for node in all_nodes:
            expected_distance = computed_distances_nx.get(node, float('inf'))
            computed_distance_step = computed_distances_step.get(node, float('inf'))

            if computed_distance_step != expected_distance:
                print(f"Test fehlgeschlagen für Knoten {node}: erwartet {expected_distance}, erhalten {computed_distance_step}")
                return False

        print("Alle Tests bestanden.")
        return True

    def test_edge_cases(self):
        edge_cases = [
            {'0': {}},
            {'0': {}, '1': {}},
            {'0': {'1': 1}, '1': {'2': 2}, '2': {'0': 3}},
            {'0': {'1': 1, '2': 4}, '1': {'2': 2}, '2': {}},
            {str(i): {str(i + 1): 1} for i in range(100)} | {str(99): {}}
        ]

        for case in edge_cases:
            self.graph = case
            self.run_dijkstra_implementation()
            if not self.test_dijkstra_algorithm(self.start_node):
                print(f"Test fehlgeschlagen für Graph: {case}")
                return False

        print("Alle Edge-Case-Tests bestanden.")
        return True


graph = {
    '0': {'1': 1, '2': 4},
    '1': {'2': 2, '3': 5},
    '2': {'3': 1},
    '3': {}
}
start_node = '0'
selected_algorithm = "Dijkstra_List"

tester = DijkstraTester(graph, start_node, selected_algorithm)
tester.run_dijkstra_implementation()
tester.test_dijkstra_algorithm(start_node)
tester.test_edge_cases()