import pygame
import sys
from pygame.locals import *

from maze import Maze

if __name__ == '__main__':
    maze = Maze()
    maze.design()
    screen = pygame.display.set_mode((maze.resX, maze.resY))
    while True:
        screen.fill((191, 191, 191))
        maze.paint(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
