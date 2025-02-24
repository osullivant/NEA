import random
from graphFINAL import Graph


class Animal:
    def __init__(self, position, speed, maxEnergy, offspringChance, offspringNum):
        self.position = position
        self.speed = speed
        self.energy = maxEnergy
        self.maxEnergy = maxEnergy
        self.offspringChance = offspringChance
        self.offspringNum = offspringNum

    def move(self, graph):
        pass  # Will be implemented in subclasses


class Predator(Animal):
    def __init__(self, position, speed, maxEnergy, offspringChance, offspringNum):
        super().__init__(position, speed, maxEnergy, offspringChance, offspringNum)

    def hunt(self, graph, preyList, predatorList):
        if random.random() < 0.8:
            preyPositions = [prey.position for prey in preyList]
            paths = graph.dijkstra(graph.getNode(self.position))

            bestPath = None
            for preyPos in preyPositions:
                if preyPos in paths and (bestPath is None or len(paths[preyPos]) < len(bestPath)):
                    bestPath = paths[preyPos]

            if bestPath:
                moveDistance = 0
                for step in bestPath:
                    if moveDistance + graph.getEdgeCost(graph.getNode(self.position), graph.getNode(step[0])) <= self.speed:
                        moveDistance += graph.getEdgeCost(graph.getNode(self.position), graph.getNode(step[0]))
                        self.position = step[0]
                        self.energy -= moveDistance
                    else:
                        break
            else:
                self.seekMate(graph, predatorList)
        else:
            self.energy += 1

    def seekMate(self, graph, predatorList):
        closestMate = None
        closestDistance = float('inf')
        paths = graph.dijkstra(graph.getNode(self.position))

        for predator in predatorList:
            if predator is not self and predator.position in paths:
                distance = len(paths[predator.position])
                if distance < closestDistance:
                    closestDistance = distance
                    closestMate = paths[predator.position]

        if closestMate:  # Always try moving toward a mate, no distance limit
            moveDistance = 0
            for step in closestMate:
                cost = graph.getEdgeCost(graph.getNode(self.position), graph.getNode(step[0]))
                if moveDistance + cost <= self.speed:
                    moveDistance += cost
                    self.position = step[0]
                    self.energy -= moveDistance
                else:
                    break


class Fox(Predator):
    def __init__(self, position):
        super().__init__(position, speed=3, maxEnergy=10, offspringChance=0.3, offspringNum=2)


class Wolf(Predator):
    def __init__(self, position):
        super().__init__(position, speed=4, maxEnergy=12, offspringChance=0.25, offspringNum=3)


class Prey(Animal):
    def __init__(self, position, speed, maxEnergy, offspringChance, offspringNum):
        super().__init__(position, speed, maxEnergy, offspringChance, offspringNum)

    def moveRandomly(self, graph):
        possibleMoves = graph.dijkstra(graph.getNode(self.position))

        validMoves = sorted(possibleMoves.keys(), key=lambda pos: len(possibleMoves[pos]), reverse=True)
        if validMoves:
            self.position = random.choice(validMoves[:3])  # Pick among the top 3 farthest moves

        if validMoves:
            self.position = random.choice(validMoves)
            self.energy -= sum(graph.getEdgeCost(graph.getNode(self.position), graph.getNode(step[0])) for step in
                               possibleMoves[self.position])


class Rabbit(Prey):
    def __init__(self, position):
        super().__init__(position, speed=2, maxEnergy=6, offspringChance=0.4, offspringNum=4)


class Deer(Prey):
    def __init__(self, position):
        super().__init__(position, speed=3, maxEnergy=8, offspringChance=0.35, offspringNum=2)


# Simulation logic
if __name__ == "__main__":
    gridSize = int(input("Enter grid size: "))
    numSteps = int(input("Enter number of steps: "))
    numPredators = int(input("Enter number of predators: "))
    numPrey = int(input("Enter number of prey: "))
    speciesChoice = input("Choose species pair (fox-rabbit or wolf-deer): ")

    graph = Graph(gridSize)

    predators = []
    preyList = []

    for _ in range(numPredators):
        startPos = random.choice(list(graph.nodeMap.keys()))
        predators.append(Fox(startPos) if speciesChoice == "fox-rabbit" else Wolf(startPos))

    for _ in range(numPrey):
        startPos = random.choice(list(graph.nodeMap.keys()))
        preyList.append(Rabbit(startPos) if speciesChoice == "fox-rabbit" else Deer(startPos))

    for _ in range(numSteps):
        for prey in preyList:
            prey.moveRandomly(graph)

        for predator in predators:
            predator.hunt(graph, preyList, predators)

        newPrey = []
        for prey in preyList:
            for otherPrey in preyList:
                if prey.position == otherPrey.position and prey is not otherPrey:
                    if random.random() < prey.offspringChance:
                        for _ in range(prey.offspringNum):
                            newPrey.append(
                                Rabbit(prey.position) if speciesChoice == "fox-rabbit" else Deer(prey.position))
        preyList.extend(newPrey)

        for predator in predators:
            for prey in preyList:
                if predator.position == prey.position:
                    predator.energy = predator.maxEnergy
                    preyList.remove(prey)

        print(f"Step completed. Predators: {len(predators)}, Prey: {len(preyList)}")
