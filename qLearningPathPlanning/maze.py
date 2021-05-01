import pygame
import numpy as np
import random


class Maze:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.cell_size = 15
        self.resX = 750
        self.resY = 750
        self.colors = [(52, 52, 52), (191, 191, 191), (43, 191, 27), (0, 123, 255)]  # black, gray, green, blue
        self.map = np.zeros((50, 50))
        self.reward = np.zeros((50, 50))
        self.target = None
        self.agent = None
        self.obstacles = []

    def paint(self, screen):
        for i in range(50):
            for j in range(50):
                pygame.draw.rect(screen, (255, 255, 255), (j * 15, i * 15, (j * 15) + 15, (i * 15) + 15), 0)
                if self.map[i, j] == -1:
                    pygame.draw.rect(screen, self.colors[0], ((j * 15) + 3, (i * 15) + 3, (j * 15) + 11, (i * 15) + 11),
                                     0)
                elif self.map[i, j] == 0:
                    pygame.draw.rect(screen, self.colors[1], ((j * 15) + 3, (i * 15) + 3, (j * 15) + 11, (i * 15) + 11),
                                     0)
                elif self.map[i, j] == 1:
                    pygame.draw.rect(screen, self.colors[3], ((j * 15) + 3, (i * 15) + 3, (j * 15) + 11, (i * 15) + 11),
                                     0)
                elif self.map[i, j] == 2:
                    pygame.draw.rect(screen, self.colors[2], ((j * 15) + 3, (i * 15) + 3, (j * 15) + 11, (i * 15) + 11),
                                     0)

    def randomObstacle(self):
        for i in range(1100):
            cell = random.randint(0, 2499)
            column = (cell % 50)
            row = int(cell / 50)
            self.obstacles.append(cell)
            self.map[row, column] = -1

        print(self.obstacles)
        self.obstacles.sort()
        print(self.obstacles)

    def createRewardMatrix(self):
        for i in range(50):
            for j in range(50):
                if self.map[i, j] == -1:
                    self.reward[i, j] = -5
                if self.map[i, j] == 0:
                    self.reward[i, j] = 3
                if self.map[i, j] == 2:
                    self.reward[i, j] = 5

    def map2txt(self):
        with open("map.txt", "w") as f:
            for i in range(50):
                for j in range(50):
                    if self.map[i, j] == -1:
                        f.write("#")
                    elif self.map[i, j] == 0:
                        f.write("-")
                    elif self.map[i, j] == 1:
                        f.write("O")
                    elif self.map[i, j] == 2:
                        f.write("X")
                f.write("\n")
