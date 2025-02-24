import heapq

class PriorityQueueTester:
    '''Programm um die eigens implementierten Heapify-Up und Down Operationen mit den bekannt korrekten von heapq zu vergleichen'''
    def __init__(self):
        self.custom_heap = []
        self.heapq_heap = []
        self.failed_tests = []

    def custom_pop_min(self):
        if not self.custom_heap:
            return None
        root = self.custom_heap[0]
        if len(self.custom_heap) == 1:
            self.custom_heap.pop()
        else:
            self.custom_heap[0] = self.custom_heap[-1]
            self.custom_heap.pop()
            self._custom_heapify_down(0)
        return root

    def custom_insert(self, element):
        self.custom_heap.append(element)
        self._custom_heapify_up(len(self.custom_heap) - 1)

    def custom_remove(self, target_node):
        for i, (_, node) in enumerate(self.custom_heap):
            if node == target_node:
                self.custom_heap[i] = ("empty", None)
                break
        self.custom_heap = [(dist, node) for dist, node in self.custom_heap if node is not None]
        self._custom_heapify_all()

    def _custom_heapify_all(self):
        n = len(self.custom_heap)
        for i in range(n // 2 - 1, -1, -1):
            self._custom_heapify_down(i)

    def _custom_heapify_down(self, index):
        n = len(self.custom_heap)
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        if left < n and self.custom_heap[left][0] < self.custom_heap[smallest][0]:
            smallest = left
        if right < n and self.custom_heap[right][0] < self.custom_heap[smallest][0]:
            smallest = right
        if smallest != index:
            self.custom_heap[index], self.custom_heap[smallest] = self.custom_heap[smallest], self.custom_heap[index]
            self._custom_heapify_down(smallest)

    def _custom_heapify_up(self, index):
        if index == 0:
            return
        parent = (index - 1) // 2
        if self.custom_heap[index][0] < self.custom_heap[parent][0]:
            self.custom_heap[index], self.custom_heap[parent] = self.custom_heap[parent], self.custom_heap[index]
            self._custom_heapify_up(parent)

    def heapq_pop_min(self):
        if not self.heapq_heap:
            return None
        return heapq.heappop(self.heapq_heap)

    def heapq_insert(self, element):
        heapq.heappush(self.heapq_heap, element)

    def heapq_remove(self, target_node):
        if target_node in [node for _, node in self.heapq_heap]:
            self.heapq_heap = [(dist, node) for dist, node in self.heapq_heap if node != target_node]
            heapq.heapify(self.heapq_heap)

    def compare_heaps(self, operation):
        if self.custom_heap != self.heapq_heap:
            print("Heaps stimmen nicht überein!")
            self.failed_tests.append(operation)
        else:
            print("Heaps stimmen überein!")
        print(f"Custom Heap: {self.custom_heap}")
        print(f"heapq Heap: {self.heapq_heap}")

    def run_tests(self):
        elements_to_insert = [
            (5, "a"),
            (3, "b"),
            (8, "c"),
            (1, "d"),
            (2, "e"),
            (7, "f"),
            (6, "g"),
            (4, "h"),
        ]
        for element in elements_to_insert:
            operation = f"Einfügen {element}"
            print(f"\n{operation}")
            print("Vor dem Einfügen:")
            self.compare_heaps(operation)
            self.custom_insert(element)
            self.heapq_insert(element)
            print("Nach dem Einfügen:")
            self.compare_heaps(operation)

        print("\nTeste pop_min Operationen:")
        for i in range(3):
            operation = f"Pop_min {i + 1}"
            print(f"\n{operation}")
            print("Vor pop_min:")
            self.compare_heaps(operation)
            custom_min = self.custom_pop_min()
            heapq_min = self.heapq_pop_min()
            print(f"Entfernt - Custom: {custom_min}, heapq: {heapq_min}")
            print("Nach pop_min:")
            self.compare_heaps(operation)
            if custom_min != heapq_min:
                print(f"Pop_min Fehler! Custom: {custom_min}, heapq: {heapq_min}")
                self.failed_tests.append(f"{operation} - Fehler")

        print("\nTeste Entfernen von spezifischen Knoten:")
        nodes_to_remove = ["b", "f", "d"]
        for target_node in nodes_to_remove:
            operation = f"Entferne Knoten {target_node}"
            print(f"\n{operation}")
            print("Vor dem Entfernen:")
            self.compare_heaps(operation)
            self.custom_remove(target_node)
            self.heapq_remove(target_node)
            print("Nach dem Entfernen:")
            self.compare_heaps(operation)

        print("\nTeste pop_min Operationen nach dem Entfernen:")
        for i in range(2):
            operation = f"Pop_min nach Entfernen {i + 1}"
            print(f"\n{operation}")
            print("Vor pop_min:")
            self.compare_heaps(operation)
            custom_min = self.custom_pop_min()
            heapq_min = self.heapq_pop_min()
            print(f"Entfernt - Custom: {custom_min}, heapq: {heapq_min}")
            print("Nach pop_min:")
            self.compare_heaps(operation)
            if custom_min != heapq_min:
                print(f"Pop_min Fehler! Custom: {custom_min}, heapq: {heapq_min}")
                self.failed_tests.append(f"{operation} - Fehler")

        if self.custom_heap or self.heapq_heap:
            operation = "Finale Heap-Überprüfung"
            print("\nHeaps sind nicht leer nach allen pop_min Operationen!")
            self.compare_heaps(operation)
        else:
            print("\nAlle Elemente erfolgreich entfernt. Heaps sind leer.")


        if not self.failed_tests:
            print("\n Alle Tests bestanden! Custom Heap verhält sich wie heapq.")
        else:
            print("\n Einige Tests fehlgeschlagen. Hier sind die fehlgeschlagenen Operationen:")
            for failed_test in self.failed_tests:
                print(f" - {failed_test}")


if __name__ == "__main__":
    tester = PriorityQueueTester()
    tester.run_tests()