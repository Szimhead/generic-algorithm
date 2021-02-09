import random
import Dot


class Population:

    def __init__(self, size):
        self.fitnessSum = 0
        self.dots = []
        self.gen = 1
        self.bestDot = 0
        self.minStep = 400
        for i in range(size):
            self.dots.append(Dot.Dot())

    def show(self):
        for i in range(1, len(self.dots)):
            self.dots[i].show()
        self.dots[0].show()

    def update(self, obstacles, checkpoints):
        for dot in self.dots:
            if dot.brain.step > self.minStep:
                dot.dead = True
            else:
                dot.update(obstacles, checkpoints)

    def calculateFitness(self):
        print("calculating fitness...")
        for dot in self.dots:
            dot.calculateFitness()

    def allDotsDead(self):
        for dot in self.dots:
            if not dot.dead and not dot.reachedGoal:
                return False
        return True

    def naturalSelection(self):
        print("natural selection...")

        newDots = []

        self.calculateFitnessSum()
        self.setBestDot()

        newDots.append(self.dots[self.bestDot].getBaby())
        newDots[0].isBest = True
        for i in range(1, len(self.dots)):
            # select parent based on fitness
            parent = self.selectParent()

            # get baby from them
            newDots.append(parent.getBaby())

        self.dots = newDots.copy()
        print("generation: " + str(self.gen))
        self.gen += 1

        if self.gen % 5 == 0:
            for dot in self.dots:
                dot.brain.increaseMoves(20)

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for dot in self.dots:
            self.fitnessSum += dot.fitness

    def selectParent(self):
        rand = random.uniform(0, self.fitnessSum)

        runningSum = 0

        for dot in self.dots:
            runningSum += dot.fitness
            if runningSum > rand:
                return dot

        return None

    def mutation(self):
        print("mutation...")

        for i in range(1, len(self.dots)):
            self.dots[i].brain.mutate()

    def setBestDot(self):
        maxDot = 0
        maxim = 0
        for i in range(len(self.dots)):
            if self.dots[i].fitness > maxim:
                maxim = self.dots[i].fitness
                maxDot = i
        self.bestDot = maxDot

        if self.dots[self.bestDot].reachedGoal:
            self.minStep = self.dots[self.bestDot].brain.step
            print(self.minStep)
