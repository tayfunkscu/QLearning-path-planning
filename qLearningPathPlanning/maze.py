import pygame
import numpy as np


class Maze:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.resX = 1000
        self.resY = 1000
        self.colors = [(52, 52, 52), (191, 191, 191), (43, 191, 27), (0, 123, 255)]  # black, gray, green, blue
        self.map = np.zeros((50, 50))
        self.target = None
        self.agent = None
        self.obstacles = None

    def design(self):
        for i in range(50):
            print("{} -> {}".format(i * 50, (i * 50) + 50))

        self.obstacles = list(map(str, input("\nSpecify the cells you would like to put an obstacle: ").split()))
        self.agent = input("Specify the starting cell for agent: ")
        self.target = input("Specify the target cell: ")

        for i in self.obstacles:
            row = int(int(i) / 50)
            column = int(i) % 50
            self.map[row, column] = -1

        row = int(int(self.agent) / 50)
        column = int(self.agent) % 50
        self.map[row, column] = 1

        row = int(int(self.target) / 50)
        column = int(self.target) % 50
        self.map[row, column] = 2

        self.map2txt()

    def paint(self, screen):
        for i in range(50):
            for j in range(50):
                pygame.draw.rect(screen, (255, 255, 255), (j * 20, i * 20, (j * 20) + 20, (i * 20) + 20), 0)
                if self.map[i, j] == -1:
                    pygame.draw.rect(screen, self.colors[0], ((j * 20) + 3, (i * 20) + 3, (j * 20) + 17, (i * 20) + 17),
                                     0)
                elif self.map[i, j] == 0:
                    pygame.draw.rect(screen, self.colors[1], ((j * 20) + 3, (i * 20) + 3, (j * 20) + 17, (i * 20) + 17),
                                     0)
                elif self.map[i, j] == 1:
                    pygame.draw.rect(screen, self.colors[3], ((j * 20) + 3, (i * 20) + 3, (j * 20) + 17, (i * 20) + 17),
                                     0)
                elif self.map[i, j] == 2:
                    pygame.draw.rect(screen, self.colors[2], ((j * 20) + 3, (i * 20) + 3, (j * 20) + 17, (i * 20) + 17),
                                     0)

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
