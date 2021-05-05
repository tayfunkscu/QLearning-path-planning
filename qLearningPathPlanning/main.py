import numpy as np
import pygame
from time import time, sleep
from random import randint as r
import random
import pickle
import sys

alpha = 0.01
gamma = 0.9
epsilon = 0

n = 15
csize = 15
scrx = n * csize
scry = n * csize
background = (51, 51, 51)
screen = pygame.display.set_mode((scrx, scry))
colors = [
    (51, 51, 51),  # gri
    (255, 0, 0),  # kırmızı
    (0, 255, 0),  # yeşil
    (143, 255, 240),  # turkuaz
]

reward = np.zeros((n, n))
obstacles = []
penalities = 10

Q = np.zeros((n ** 2, 4))
actions = {"up": 0, "down": 1, "left": 2, "right": 3}
states = {}


def settings():
    global reward, penalities, target, obstacles, agent_starting_position, n

    reward[target[0], target[1]] = 5

    while penalities != 0:
        i = r(0, n - 1)
        j = r(0, n - 1)
        if reward[i, j] == 0 and [i, j] != agent_starting_position and [i, j] != target:
            reward[i, j] = -5
            penalities -= 1
            obstacles.append(n * i + j)

    for i in range(n):
        for j in range(n):
            if reward[i, j] == 0:
                reward[i, j] == 3

    reward[agent_starting_position[0], agent_starting_position[1]] = 0

    k = 0
    for i in range(n):
        for j in range(n):
            states[(i, j)] = k
            k += 1


def layout():
    for i in range(n):
        for j in range(n):
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (j * csize, i * csize, (j * csize) + csize, (i * csize) + csize),
                0,
            )

            pygame.draw.rect(
                screen,
                colors[0],
                (
                    (j * csize) + 3,
                    (i * csize) + 3,
                    (j * csize) + 11,
                    (i * csize) + 11,
                ),
                0,
            )

            if reward[i, j] == -5:
                pygame.draw.rect(
                    screen,
                    colors[1],
                    (
                        (j * csize) + 3,
                        (i * csize) + 3,
                        (j * csize) + 11,
                        (i * csize) + 11,
                    ),
                    0,
                )
            if reward[i, j] == 5:
                pygame.draw.rect(
                    screen,
                    colors[2],
                    (
                        (j * csize) + 3,
                        (i * csize) + 3,
                        (j * csize) + 11,
                        (i * csize) + 11,
                    ),
                    0,
                )


def select_action(current_state):
    global current_pos, epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        if current_pos[1] != 0:
            possible_actions.append("left")
        if current_pos[1] != n - 1:
            possible_actions.append("right")
        if current_pos[0] != 0:
            possible_actions.append("up")
        if current_pos[0] != n - 1:
            possible_actions.append("down")
        action = actions[possible_actions[r(0, len(possible_actions) - 1)]]
    else:
        m = np.min(Q[current_state])
        if current_pos[0] != 0:
            possible_actions.append(Q[current_state, 0])
        else:
            possible_actions.append(m - 100)
        if current_pos[0] != n - 1:
            possible_actions.append(Q[current_state, 1])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != 0:
            possible_actions.append(Q[current_state, 2])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != n - 1:
            possible_actions.append(Q[current_state, 3])
        else:
            possible_actions.append(m - 100)

        action = random.choice(
            [i for i, a in enumerate(possible_actions) if a == max(possible_actions)]
        )
        return action


def episode():
    global current_pos, epsilon, agent_starting_position
    current_state = states[(current_pos[0], current_pos[1])]
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
    if new_state not in obstacles:
        Q[current_state, action] = reward[
            current_pos[0], current_pos[1]
        ] + gamma * np.max(Q[new_state])
    else:
        Q[current_state, action] = reward[
            current_pos[0], current_pos[1]
        ] + gamma * np.max(Q[new_state])
        current_pos = agent_starting_position
        epsilon -= 1e-3


agent_starting_position = list(
    map(int, input("Agent starting position(row,col): ").split(","))
)

current_pos = agent_starting_position

target = list(map(int, input("Target position(row,col): ").split(",")))

settings()

while True:
    screen.fill(background)
    layout()
    pygame.draw.circle(
        screen,
        (25, 129, 230),
        (current_pos[1] * csize + 8, current_pos[0] * csize + 8),
        4,
        0,
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    episode()

print(epsilon)
