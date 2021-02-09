import main
import pygame
import numpy as np
import math
from Brain import Brain


class Dot:

    def __init__(self):
        self.brain = Brain(30)
        self.pos = (main.WIDTH / 2, main.HEIGHT - 200)
        self.vel = (0, 0)
        self.acc = (0, 0)
        self.dead = False
        self.reachedGoal = False
        self.fitness = 0
        self.isBest = False
        self.checkpointsReached = 0
        self.checkpoints = []

    def show(self):
        if self.isBest:
            dot = pygame.Rect(self.pos[0], self.pos[1], 8, 8)
            pygame.draw.rect(main.WIN, main.GREEN, dot)
        else:
            dot = pygame.Rect(self.pos[0], self.pos[1], 4, 4)
            pygame.draw.rect(main.WIN, main.YELLOW, dot)

    def move(self):
        if len(self.brain.directions) > self.brain.step:
            self.acc = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            self.dead = True

        self.vel = np.add(self.vel, self.acc)
        if self.vel[0] > 5:
            self.vel[0] = 5
        elif self.vel[0] < -5:
            self.vel[0] = -5
        if self.vel[1] > 5:
            self.vel[1] = 5
        elif self.vel[1] < -5:
            self.vel[1] = -5

        self.pos = np.add(self.vel, self.pos)

    def update(self, obstacles, checkpoints):
        if not self.dead and not self.reachedGoal:
            self.move()

            if self.pos[0] < 10 or self.pos[1] < 10 or self.pos[0] > main.WIDTH - 10 or self.pos[1] > main.HEIGHT - 10:
                self.dead = True
            elif math.sqrt(((self.pos[0]-main.goal.center[0])**2)+((self.pos[1]-main.goal.center[1])**2)) < 10:
                self.reachedGoal = True

            for obs in obstacles:
                if obs.colliderect(pygame.Rect(self.pos[0], self.pos[1], 8, 8)):
                    self.dead = True

            for check in checkpoints:
                if check.colliderect(pygame.Rect(self.pos[0], self.pos[1], 8, 8)) and check not in self.checkpoints:
                    self.checkpointsReached += 1
                    self.checkpoints.append(check)

    def calculateFitness(self):
        if self.reachedGoal:
            self.fitness = 1.0/8.0 + 1000.0/(self.brain.step * self.brain.step)
        else:
            distanceToGoal = math.sqrt(((self.pos[0]-main.goal.center[0])**2)+((self.pos[1]-main.goal.center[1])**2))
            self.fitness = 1.0/(distanceToGoal * distanceToGoal)
            self.fitness += (self.checkpointsReached * self.checkpointsReached)/1000

    def getBaby(self):
        baby = Dot()
        baby.brain = self.brain.clone()
        return baby
