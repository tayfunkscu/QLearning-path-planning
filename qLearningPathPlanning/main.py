import pygame
import sys
import random
import numpy as np
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

from maze import Maze

maze = Maze()
screen = pygame.display.set_mode((maze.resX, maze.resY))
selection = True
ready = True
gamma = 0.9
alpha = 0.01

Q = np.zeros((50 ** 2, 4))
current_pos = [0, 0]
start_pos = [0, 0]
actions = {"up": 0, "down": 1, "left": 2, "right": 3}
states = {}
k = 0
for i in range(50):
    for j in range(50):
        states[(i, j)] = k
        k += 1

Tk().wm_withdraw()
messagebox.showinfo("Instructions",
                    "Create random obstacles: Press R\nSelect agent starting point: Left Click\nSelect target point: Right Click\nSave changes : Press Q")

epsilon = 0.25


def select_action(current_state):
    global current_pos, epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        if current_pos[1] != 0:
            possible_actions.append("left")
        if current_pos[1] != 50 - 1:
            possible_actions.append("right")
        if current_pos[0] != 0:
            possible_actions.append("up")
        if current_pos[0] != 50 - 1:
            possible_actions.append("down")
        action = actions[possible_actions[random.randint(0, len(possible_actions) - 1)]]
    else:
        m = np.min(Q[current_state])
        if current_pos[0] != 0:
            possible_actions.append(Q[current_state, 0])
        else:
            possible_actions.append(m - 100)
        if current_pos[0] != 50 - 1:
            possible_actions.append(Q[current_state, 1])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != 0:
            possible_actions.append(Q[current_state, 2])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != 50 - 1:
            possible_actions.append(Q[current_state, 3])
        else:
            possible_actions.append(m - 100)

        action = random.choice([i for i, a in enumerate(possible_actions) if a == max(possible_actions)])
        return action


def episode(maze):
    global current_pos, epsilon
    current_state = states[(current_pos[0], current_pos[1])]
    print("----------------")
    print(current_pos[0], current_pos[1])
    print(current_state)
    action = select_action(current_state)
    if action == 0:
        current_pos[0] -= 1
    elif action == 1:
        current_pos[0] += 1
    elif action == 2:
        current_pos[1] -= 1
    elif action == 3:
        current_pos[1] += 1
    new_state = states[(current_pos[0], current_pos[1])]
    print(current_pos[0], current_pos[1])
    print(new_state)
    if new_state not in maze.obstacles:
        Q[current_state, action] += alpha * (
                maze.reward[current_pos[0], current_pos[1]] + gamma * (np.max(Q[new_state])) - Q[
            current_state, action])
        # Q[current_state,action] = (reward[current_pos[0],current_pos[1]] + gamma*(np.max(Q[new_state])) - Q[current_state,action])
    else:
        Q[current_state, action] += alpha * (maze.reward[current_pos[0], current_pos[1]] - Q[current_state, action])
        current_pos = start_pos
        epsilon -= 1e-3


while True:
    screen.fill((191, 191, 191))
    maze.paint(screen)
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (250, 15, 152), (current_pos[1] * 15 + 8, current_pos[0] * 15 + 8), 4, 0)
    for event in pygame.event.get():
        if event.type == QUIT:
            maze.map2txt()
            pygame.quit()
            sys.exit()

        if ready:
            if selection:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    cor_y, cor_x = event.pos
                    current_pos = [int(cor_x / 15), int(cor_y / 15)]
                    start_pos = [int(cor_x / 15), int(cor_y / 15)]
                    print(current_pos)
                    maze.map[int(cor_x / 15), int(cor_y / 15)] = 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                    cor_y, cor_x = event.pos
                    maze.map[int(cor_x / 15), int(cor_y / 15)] = 2
                if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "r":
                    maze.randomObstacle()
        else:
            episode(maze)

        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "q":
            maze.createRewardMatrix()
            ready = False

    pygame.display.update()
