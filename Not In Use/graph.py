class Graph:
    def __init__(self):
        self.nodes = []
        self.connCosts = {}

    def addNode(self, node):
        if type(node) != Node:
            print("Node must be Node object")
            return -1
        self.nodes.append(node)

    def addEdge(self, node1, node2, cost, primDirection):
        primDirection = primDirection.upper()
        inverse = {"DOWN": "UP",
                   "UP": "DOWN",
                   "RIGHT": "LEFT",
                   "LEFT": "RIGHT"}
        node1.addConnection(node2, cost, primDirection)
        node2.addConnection(node1, cost, inverse[primDirection])
        if node1 in self.connCosts.keys():
            if node2 in self.connCosts[node1]:
                print("Nodes already connected")
                return -1
            current = list(self.connCosts[node1])
            current.append(node2)
            self.connCosts[node1] = current
        else:
            self.connCosts[node1] = [node2]
        if node2 in self.connCosts.keys():
            if node1 in self.connCosts[node2]:
                print("Nodes already connected")
                return -1
            current = list(self.connCosts[node2])
            current.append(node1)
            self.connCosts[node2] = current
        else:
            self.connCosts[node2] = [node1]

    def getCost(self, node1, node2):
        if node1 in self.connCosts.keys() and node2 in self.connCosts[node1]:
            return node1.connCosts[node2]
        else:
            print(f"Nodes {node1.label} and {node2.label} not connected")
            return -1

    def getConnected(self, node, labels=0):
        keys = list(node.connCosts.keys())
        if labels != 0:
            newL = []
            for key in keys:
                newL.append(key.label)
            return newL
        return keys

    def getCosts(self, node):
        return list(node.connCosts.values())

    def getConnectedWithCosts(self, node, labels=0):
        l1 = self.getConnected(node, labels)
        l2 = self.getCosts(node)
        l3 = []
        for i in range(len(l1)):
            l3.append((l1[i], l2[i]))
        return l3

    def getConnectedWithDirections(self, node, labels=0):
        return node.getConnectedDir(labels)


class Node:
    def __init__(self, label):
        self.label = label
        self.connCosts = {self: 0}
        self.connectedNodes = {"UP": None,
                               "DOWN": None,
                               "LEFT": None,
                               "RIGHT": None}

    def getLabel(self):
        return self.label

    def getConnectedDir(self, labels=0):
        l1 = []
        for key in self.connectedNodes.keys():
            val = self.connectedNodes[key]
            if val is not None:
                l1.append(key)
                if labels == 1:
                    l1.append(val.label)
                else:
                    l1.append(val)
        return l1

    def addConnection(self, node2, cost, direction):
        self.connectedNodes[direction.upper()] = node2
        self.connCosts[node2] = cost


if __name__ == "__main__":
    n1 = Node("A")
    n2 = Node("B")
    n3 = Node("C")
    g = Graph()
    g.addNode(n1)
    g.addNode(n2)
    g.addEdge(n1, n2, 5, "LEFT")
    g.addNode(n3)
    g.addEdge(n1, n3, 1, "DOWN")
    print(g.getCost(n2, n3))
    # print(g.getConnected(n1))
    print(g.getConnected(n1, 1))
    # print(g.getConnectedWithCosts(n1))
    print(g.getConnectedWithCosts(n1, 1))
    print(g.getConnectedWithDirections(n1))
