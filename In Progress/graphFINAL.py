import sys


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def isEmpty(self):
        return len(self.elements) == 0

    def enqueue(self, item, priority):
        self.elements.append((priority, item))
        self.elements.sort(key=lambda x: x[0])  # Sort by priority

    def dequeue(self):
        return self.elements.pop(0)[1]  # Remove and return item with lowest priority


class Node:
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.position = f"{chr(97 + x)}{y + 1}"  # 'a1', 'b2', etc.
        self.value = value if value else "empty"
        self.neighbors = {}  # Stores adjacent nodes with weights

    def __repr__(self):
        return f"Node({self.position}, Value: {self.value})"


class Graph:
    def __init__(self, n):
        self.n = n
        self.nodes = [[Node(x, y) for y in range(n)] for x in range(n)]
        self.nodeMap = {node.position: node for row in self.nodes for node in row}
        self._connectNodes()

    def _connectNodes(self):
        for x in range(self.n):
            for y in range(self.n):
                node = self.nodes[x][y]
                if x > 0:
                    node.neighbors[self.nodes[x - 1][y]] = 1  # Left
                if x < self.n - 1:
                    node.neighbors[self.nodes[x + 1][y]] = 1  # Right
                if y > 0:
                    node.neighbors[self.nodes[x][y - 1]] = 1  # Up
                if y < self.n - 1:
                    node.neighbors[self.nodes[x][y + 1]] = 1  # Down

    def getNode(self, identifier):
        return self.nodeMap.get(identifier)

    def setValue(self, position, value):
        node = self.getNode(position)
        if node:
            node.value = value

    def getEdgeCost(self, nodeA, nodeB):
        return nodeA.neighbors.get(nodeB, float('inf'))

    def heuristic(self, node, goal):
        return abs(node.x - goal.x) + abs(node.y - goal.y)  # Manhattan distance

    def aStar(self, start, end):
        openList = [start]
        cameFrom = {}
        gScore = {node: float('inf') for row in self.nodes for node in row}
        gScore[start] = 0
        fScore = {node: float('inf') for row in self.nodes for node in row}
        fScore[start] = self.heuristic(start, end)

        while openList:
            openList.sort(key=lambda node: fScore[node])  # Sort by fScore
            current = openList.pop(0)

            if current == end:
                path = []
                while current in cameFrom:
                    path.append((current.position, current.value))
                    current = cameFrom[current]
                return path[::-1]

            for neighbor, weight in current.neighbors.items():
                tentativeGScore = gScore[current] + weight
                if tentativeGScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentativeGScore
                    fScore[neighbor] = tentativeGScore + self.heuristic(neighbor, end)
                    if neighbor not in openList:
                        openList.append(neighbor)

        return None  # No path found

    def dijkstra(self, start):
        pq = PriorityQueue()
        pq.enqueue(start, 0)
        distances = {node: float('inf') for row in self.nodes for node in row}
        distances[start] = 0
        previousNodes = {}

        while not pq.isEmpty():
            current = pq.dequeue()

            for neighbor, weight in current.neighbors.items():
                alt = distances[current] + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previousNodes[neighbor] = current
                    pq.enqueue(neighbor, alt)

        shortestPaths = {}
        for node in distances:
            path = []
            current = node
            while current in previousNodes:
                path.append((current.position, current.value))
                current = previousNodes[current]
            if path:
                shortestPaths[node.position] = path[::-1]

        return shortestPaths


if __name__ == "__main__":
    graph = Graph(5)
    graph.setValue("a1", "Fox")
    graph.setValue("e5", "Rabbit")
    startNode = graph.getNode("a1")

    print("Dijkstra's Paths:", graph.dijkstra(startNode))
