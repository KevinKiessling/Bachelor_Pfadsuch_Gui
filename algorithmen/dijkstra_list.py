import heapq


class Dijkstra_List():
    def __init__(self):
        super().__init__()



    #dijkstra algorithmus mit priority Queue
    def run_dijkstra_list(self, graph, startnode):


        distances = {node: float('inf') for node in graph}
        distances[startnode] = 0
        node_in_queue = {startnode: 0}

        priority_queue = [(0, startnode)]

        visited = set()
        visited_edges = set()
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node in visited:
                continue

            visited.add(current_node)
            node_in_queue.pop(current_node, None)

            for neighbor, edge_weight in graph[current_node].items():

                new_distance = current_distance + edge_weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

                    if neighbor not in node_in_queue or new_distance < node_in_queue[neighbor]:
                        heapq.heappush(priority_queue, (new_distance, neighbor))
                        node_in_queue[neighbor] = new_distance  # Update tracking
                        visited_edges.add((current_node, neighbor))


        return distances