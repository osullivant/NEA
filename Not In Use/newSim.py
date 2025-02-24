import datetime
import math
import time
import pygame
import random
from graph2 import Node, Graph, create_grid


class Animal:
    def __init__(self, x, y, speed, maxEnergy, offspringChance, offspringNum):
        self.speed = speed
        self.hunger = 100
        self.x, self.y = x, y
        self.isDead = False
        self.offspringChance = offspringChance
        self.offspringNum = offspringNum

    def move(self, xDist, yDist):
        self.x += xDist
        self.y += yDist

    def moveRandomly(self):
        xDir = random.choice([-1, 1])
        yDir = random.choice([-1, 1])
        xDist = random.randint(0, self.speed) * xDir
        yDist = random.randint(0, round(math.sqrt(self.speed ** 2 - abs(xDist) ** 2))) * yDir
        print(f"Dist: {xDist, yDist} = {math.sqrt(xDist ** 2 + yDist ** 2)}")
        self.move(xDist, yDist)

    def getCoords(self):
        return self.x, self.y

    def changeHunger(self, value):
        self.hunger += value
        if self.hunger <= 0:
            self.starve()

    def starve(self):
        self.isDead = True


class Predator(Animal):
    def __init__(self, x, y, speed, maxEnergy, offspringChance, offspringNum):
        super().__init__(x, y, speed, maxEnergy, offspringChance, offspringNum)


class Prey(Animal):
    def __init__(self, x, y, speed, maxEnergy, offspringChance, offspringNum):
        super().__init__(x, y, speed, maxEnergy, offspringChance, offspringNum)


class Fox(Predator):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 2, 50, 0.05, 4)


class Wolf(Predator):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 3, 100, 0.05, 5)


class Deer(Prey):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 5, 0.2, 75, 2)


class Rabbit(Prey):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 4, 25, 0.15, 7)


if __name__ == "__main__":
    grid = Graph()
    create_grid(grid, 5, 5, [1, 2, 2, 2, 3, 3])
    print(grid)
