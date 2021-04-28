import pygame
import sys
from pygame.locals import *

from maze import Maze

maze = Maze()
screen = pygame.display.set_mode((maze.resX, maze.resY))
selection = True
while True:
    screen.fill((191, 191, 191))
    maze.paint(screen)
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            maze.map2txt()
            pygame.quit()
            sys.exit()
        if selection:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                cor_y, cor_x = event.pos
                maze.map[int(cor_x / 15), int(cor_y / 15)] = 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                cor_y, cor_x = event.pos
                maze.map[int(cor_x / 15), int(cor_y / 15)] = 2
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                selection = False
        else:
            cor_y, cor_x = mouse_pos
            maze.map[int(cor_x / 15), int(cor_y / 15)] = -1 if maze.map[int(cor_x / 15), int(cor_y / 15)] == 0 else \
                maze.map[int(cor_x / 15), int(cor_y / 15)]
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click

    pygame.display.update()
