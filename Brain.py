import random
import numpy


class Brain:
    def __init__(self, size):
        self.directions = []
        self.step = 0
        self.randomize(size)

    def randomize(self, size):
        for i in range(size):
            randomAngle = random.uniform(0, 2 * numpy.pi)
            self.directions.append((numpy.cos(randomAngle), numpy.sin(randomAngle)))

    def clone(self):
        clone = Brain(len(self.directions))
        clone.directions = []
        clone.step = 0

        for i in range(len(self.directions)):
            clone.directions.append(self.directions[i])

        return clone

    def mutate(self):
        mutationRate = 0.01
        for i in range(len(self.directions)):
            rand = random.random()
            if rand < mutationRate:
                randomAngle = random.uniform(0, 2 * numpy.pi)
                self.directions[i] = (numpy.cos(randomAngle), numpy.sin(randomAngle))

    def increaseMoves(self, moves):
        for i in range(len(self.directions), len(self.directions) + moves):
            randomAngle = random.uniform(0, 2 * numpy.pi)
            self.directions.append((numpy.cos(randomAngle), numpy.sin(randomAngle)))
