import random
import string
import heapq


class Node:
    def __init__(self, gridValue, contents="Empty"):
        self._gridValue = gridValue  # Fixed grid-style value (e.g., A1)
        self._contents = contents  # Changeable content (e.g., "Empty", "Animal", "Fox", "Rabbit")

    def __str__(self):
        return f"{self._gridValue} ({self._contents})"

    def getGridValue(self):
        return self._gridValue

    def getContent(self):
        return self._contents

    def setContent(self, newContent):
        self._contents = newContent


class Graph:
    def __init__(self):
        self._adjList = {}
        self._edgeCosts = {}

    def __str__(self):
        returnDict = self.getGraphInfo()
        returnStr = "\nAdj Matrix: \n"
        for conn in returnDict["matrix"]:
            returnStr += f"{conn}: {returnDict['matrix'][conn]} \n"

        returnStr += "\nEdge Costs: \n"
        seenEdges = set()
        for (v1, v2), cost in returnDict["costs"].items():
            if (v2, v1) not in seenEdges:
                returnStr += f"({v1}, {v2}): {cost} \n"
                seenEdges.add((v1, v2))

        return returnStr

    def getGraphInfo(self):
        return {"matrix": self.getAdjMatrixLabeled(), "costs": self.getEdgeCosts()}

    def getAdjMatrix(self):
        return self._adjList

    def getAdjMatrixLabeled(self):
        return {vertex.getGridValue(): [neighbor.getGridValue() for neighbor in neighbors]
                for vertex, neighbors in self._adjList.items()}

    def getEdgeCosts(self):
        return {(v1.getGridValue(), v2.getGridValue()): cost
                for (v1, v2), cost in self._edgeCosts.items()}

    def addVertex(self, vertex):
        self._adjList.setdefault(vertex, [])

    def addEdge(self, vertex1, vertex2, cost=1):
        if vertex1 in self._adjList and vertex2 in self._adjList:
            self._adjList[vertex1].append(vertex2)
            self._adjList[vertex2].append(vertex1)  # For undirected graph
            self._edgeCosts[(vertex1, vertex2)] = cost
            self._edgeCosts[(vertex2, vertex1)] = cost

    def removeEdge(self, vertex1, vertex2):
        if vertex1 in self._adjList and vertex2 in self._adjList:
            self._adjList[vertex1].remove(vertex2)
            self._adjList[vertex2].remove(vertex1)
            self._edgeCosts.pop((vertex1, vertex2), None)
            self._edgeCosts.pop((vertex2, vertex1), None)

    def removeVertex(self, vertex):
        if vertex in self._adjList:
            for adjacent in self._adjList[vertex]:
                self._adjList[adjacent].remove(vertex)
                self._edgeCosts.pop((vertex, adjacent), None)
                self._edgeCosts.pop((adjacent, vertex), None)
            del self._adjList[vertex]

    def updateNodeContent(self, gridValue, newContent):
        for node in self._adjList:
            if node.getGridValue() == gridValue:
                node.setContent(newContent)
                return f"Node {gridValue} updated to {newContent}."
        return f"Node {gridValue} not found."

    def getEdgeCost(self, gridValue1, gridValue2):
        nodes = {node.getGridValue(): node for node in self._adjList}
        node1, node2 = nodes.get(gridValue1), nodes.get(gridValue2)
        if node1 and node2:
            return self._edgeCosts.get((node1, node2), self._edgeCosts.get((node2, node1), f"No edge found between {gridValue1} and {gridValue2}."))
        return f"One or both nodes {gridValue1} and {gridValue2} not found."

    def getNode(self, gridValue):
        for node in self._adjList:
            if node.getGridValue() == gridValue:
                return node
        return None  # Return None if the node is not found


def createGrid(graph: Graph, rows: int, cols: int, costProbs: list):
    nodes = {}
    letters = string.ascii_uppercase[:rows]

    for i in range(rows):
        for j in range(cols):
            gridValue = f"{letters[i]}{j + 1}"
            node = Node(gridValue)
            nodes[(i, j)] = node
            graph.addVertex(node)

    for i in range(rows):
        for j in range(cols):
            if j < cols - 1:
                graph.addEdge(nodes[(i, j)], nodes[(i, j + 1)], random.choice(costProbs))
            if i < rows - 1:
                graph.addEdge(nodes[(i, j)], nodes[(i + 1, j)], random.choice(costProbs))


def dijkstra(self, start):
    pq = [(0, start)]  # Priority queue (cost, node)
    distances = {node: float('inf') for node in self._adjList}
    distances[start] = 0

    while pq:
        currentCost, currentNode = heapq.heappop(pq)

        for neighbor in self._adjList[currentNode]:
            edgeCost = self._edgeCosts[(currentNode, neighbor)]
            newCost = currentCost + edgeCost
            if newCost < distances[neighbor]:
                distances[neighbor] = newCost
                heapq.heappush(pq, (newCost, neighbor))

    return {node.getGridValue(): cost for node, cost in distances.items()}


def aStar(self, start, end, heuristic):
    pq = [(0, start)]  # Priority queue (cost, node)
    gCosts = {node: float('inf') for node in self._adjList}
    gCosts[start] = 0
    fCosts = {node: float('inf') for node in self._adjList}
    fCosts[start] = heuristic(start, end)
    previousNodes = {}

    while pq:
        _, currentNode = heapq.heappop(pq)
        if currentNode == end:
            path = []
            while currentNode in previousNodes:
                path.append(currentNode.getGridValue())
                currentNode = previousNodes[currentNode]
            return path[::-1] + [end.getGridValue()]

        for neighbor in self._adjList[currentNode]:
            edgeCost = self._edgeCosts[(currentNode, neighbor)]
            newGCost = gCosts[currentNode] + edgeCost
            if newGCost < gCosts[neighbor]:
                gCosts[neighbor] = newGCost
                fCosts[neighbor] = newGCost + heuristic(neighbor, end)
                previousNodes[neighbor] = currentNode
                heapq.heappush(pq, (fCosts[neighbor], neighbor))

    return None  # No path found


if __name__ == "__main__":
    graph = Graph()
    createGrid(graph, 5, 5, [1, 2, 2, 2, 3, 3])

    print(graph.updateNodeContent("A1", "Fox"))
    print(graph.updateNodeContent("B2", "Rabbit"))
    print(graph.updateNodeContent("Z10", "Fox"))
    print(dijkstra(graph, graph.getNode("A1")))
    # print(graph)
