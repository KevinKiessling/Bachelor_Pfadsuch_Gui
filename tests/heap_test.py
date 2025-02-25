import heapq


class PriorityQueueTester:
    """Programm um die eigens implementierten Heapify-Up und Down Operationen mit den bekannt korrekten von heapq zu vergleichen"""

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
                self.custom_heap[i] = self.custom_heap[-1]
                self.custom_heap.pop()
                self._custom_heapify_down(i)
                self._custom_heapify_up(i)
                break

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
        self.heapq_heap = [(dist, node) for dist, node in self.heapq_heap if node != target_node]
        heapq.heapify(self.heapq_heap)

    def is_valid_heap(self, heap):
        n = len(heap)
        for i in range(n // 2):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and heap[left][0] < heap[i][0]:
                return False
            if right < n and heap[right][0] < heap[i][0]:
                return False
        return True

    def compare_heaps(self, operation, strict=True):
        if strict:
            if self.custom_heap != self.heapq_heap:
                print(f"Fehler bei {operation}: Heaps stimmen nicht überein!")
                self.failed_tests.append(operation)
            else:
                print(f"{operation} erfolgreich: Heaps stimmen überein.")
        else:
            if not self.is_valid_heap(self.custom_heap):
                print(f"Fehler bei {operation}: Custom Heap ist nicht valide!")
                self.failed_tests.append(operation)
            else:
                print(f"{operation} erfolgreich: Custom Heap ist valide.")

    def run_tests(self):
        elements_to_insert = [(5, "a"), (3, "b"), (8, "c"), (1, "d"), (2, "e"), (7, "f"), (6, "g"), (4, "h")]

        for element in elements_to_insert:
            operation = f"Einfügen {element}"
            self.custom_insert(element)
            self.heapq_insert(element)
            self.compare_heaps(operation)

        for _ in range(3):
            operation = "Pop_min"
            custom_min = self.custom_pop_min()
            heapq_min = self.heapq_pop_min()
            if custom_min != heapq_min:
                print(f"Fehler bei {operation}: Custom: {custom_min}, heapq: {heapq_min}")
                self.failed_tests.append(operation)
            else:
                print(f"{operation} erfolgreich: Beide Heaps haben {custom_min} entfernt.")

        nodes_to_remove = ["b", "f", "d"]
        for target_node in nodes_to_remove:
            operation = f"Entferne Knoten {target_node}"
            self.custom_remove(target_node)
            self.heapq_remove(target_node)
            self.compare_heaps(operation, strict=False)

        for _ in range(2):
            operation = "Pop_min nach Entfernen"
            custom_min = self.custom_pop_min()
            heapq_min = self.heapq_pop_min()
            if custom_min != heapq_min:
                print(f"Fehler bei {operation}: Custom: {custom_min}, heapq: {heapq_min}")
                self.failed_tests.append(operation)
            else:
                print(f"{operation} erfolgreich: Beide Heaps haben {custom_min} entfernt.")

        if not self.failed_tests:
            print("\nAlle Tests bestanden! Custom Heap verhält sich wie heapq.")
        else:
            print("\nEinige Tests fehlgeschlagen:")
            for failed_test in self.failed_tests:
                print(f" - {failed_test}")


if __name__ == "__main__":
    tester = PriorityQueueTester()
    tester.run_tests()
