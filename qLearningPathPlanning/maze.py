import pygame
import numpy as np


class Maze:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.cell_size = 15
        self.resX = 750
        self.resY = 750
        self.colors = [(52, 52, 52), (191, 191, 191), (43, 191, 27), (0, 123, 255)]  # black, gray, green, blue
        self.map = np.zeros((50, 50))
        self.target = None
        self.agent = None
        self.obstacles = None

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
