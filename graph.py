import math

class Graph:

    def __init__(self):
        self.nodes = {}

    def add_node(self, id):
        self.nodes[id] = []

    def remove_node(self, id):
        self.nodes.pop(id)

    def add_edge(self, node1, node2, weight):
        self.nodes[node1].append((node2, weight))
        self.nodes[node2].append((node1, weight))

    def edit_edge(self, node1, node2, weight):
        self.remove_edge(node1, node2)
        self.add_edge(node1, node2, weight)

    def remove_edge(self, node1, node2):
        for edge in self.nodes[node1]:
            if edge[0] == node2:
                self.nodes[node1].remove(edge)
        
        for edge in self.nodes[node2]:
            if edge[0] == node1:
                self.nodes[node2].remove(edge)

    def dijkstra(self, start):
        unvisited = list(self.nodes.keys())
        distances = {node : math.inf for node in unvisited}
        distances[start] = 0

        while len(unvisited) > 0:
            if min(map(lambda x : distances[x], unvisited)) == math.inf:
                break
            currentNode = min(unvisited, key=lambda y : distances[y])
            currentDst = distances[currentNode]
            for edge in self.nodes[currentNode]:
                if edge[0] in unvisited:
                    dst = currentDst + edge[1]
                    if dst < distances[edge[0]]:
                        distances[edge[0]] = dst
            unvisited.remove(currentNode)

        print(distances)


# x = Graph()
# for i in range(1, 7):
#     x.add_node(i)

# x.add_edge(1, 2, 5)
# x.add_edge(1, 3, 6)
# x.add_edge(1, 4, 2)
# x.add_edge(2, 5, 4)
# x.add_edge(3, 4, 2)
# x.add_edge(3, 5, 4)
# x.add_edge(3, 6, 8)
# x.add_edge(4, 6, 12)
# x.add_edge(5, 6, 3)

# x.dijkstra(1)
