import numpy as np
import pygame
from time import time, sleep
import matplotlib.pyplot as plt
from random import randint as r
import random
import pickle
import sys
from PyQt5 import QtWidgets
from numba import jit, cuda

agent_starting_position = [2, 2]
n = 10
target = [5, 5]
penalities = 20
path_value = -0.1

gamma = 0.9
epsilon = 0.5
csize = 15
scrx = n * csize
scry = n * csize
background = (51, 51, 51)
colors = [
    (51, 51, 51),  # gri
    (255, 0, 0),  # kırmızı
    (0, 255, 0),  # yeşil
    (143, 255, 240),  # turkuaz
]

reward = np.zeros((n, n))
obstacles = []

Q = np.zeros((n ** 2, 4))
actions = {"up": 0, "down": 1, "left": 2, "right": 3}
states = {}
sumOfRewards = []
episodeViaStep = []
step = 0
temp = 0
highestReward = 0
highestReward_counter = 0
shortest_path = []
repeatLimit = 50


class QLearningSettings(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QLearningSettings, self).__init__(parent)

        layout = QtWidgets.QFormLayout()

        self.btn = QtWidgets.QPushButton("Matrix Size")
        self.btn.clicked.connect(self.matrixSize)
        self.le = QtWidgets.QLineEdit()
        self.le.setPlaceholderText("15")
        layout.addRow(self.btn, self.le)

        self.btn1 = QtWidgets.QPushButton("Agent Starting Position")
        self.btn1.clicked.connect(self.starting_position)
        self.le1 = QtWidgets.QLineEdit()
        self.le1.setPlaceholderText("5,5")
        layout.addRow(self.btn1, self.le1)

        self.btn2 = QtWidgets.QPushButton("Target Position")
        self.btn2.clicked.connect(self.target_position)
        self.le2 = QtWidgets.QLineEdit()
        self.le2.setPlaceholderText("10,10")
        layout.addRow(self.btn2, self.le2)

        self.btn3 = QtWidgets.QPushButton("Obstacle Percentage")
        self.btn3.clicked.connect(self.obstacle_percentage)
        self.le3 = QtWidgets.QLineEdit()
        self.le3.setPlaceholderText("40")
        layout.addRow(self.btn3, self.le3)

        self.btn4 = QtWidgets.QPushButton("Epsilon Value")
        self.btn4.clicked.connect(self.epsilon_value)
        self.le4 = QtWidgets.QLineEdit()
        self.le4.setPlaceholderText("0.50")
        layout.addRow(self.btn4, self.le4)

        self.btn5 = QtWidgets.QPushButton("Path Value")
        self.btn5.clicked.connect(self.path_value)
        self.le5 = QtWidgets.QLineEdit()
        self.le5.setPlaceholderText("-0.1")
        layout.addRow(self.btn5, self.le5)

        self.btn3 = QtWidgets.QPushButton("OK")
        self.btn3.clicked.connect(self.ex)
        layout.addRow(self.btn3)

        self.setLayout(layout)
        self.setWindowTitle("Q Learning Settings")

    def matrixSize(self):
        num, ok = QtWidgets.QInputDialog.getInt(
            self, "Matrix Size", "Enter Matrix Size:")

        if ok:
            self.le.setText(str(num))

    def starting_position(self):

        text, ok = QtWidgets.QInputDialog.getText(
            self, 'Agent Starting Position', 'Enter Agent Starting Position:')

        if ok:
            self.le1.setText(str(text))

    def target_position(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self, 'Target Position', 'Enter Target Position:')

        if ok:
            self.le2.setText(str(text))

    def obstacle_percentage(self):
        num, ok = QtWidgets.QInputDialog.getInt(
            self, "Obstacle Percentage", "Enter Obstacle Percentage:")

        if ok:
            self.le3.setText(str(num))

    def epsilon_value(self):
        num, ok = QtWidgets.QInputDialog.getInt(
            self, "Epsilon Value", "Enter Epsilon Value:")

        if ok:
            self.le4.setText(str(num))

    def path_value(self):
        num, ok = QtWidgets.QInputDialog.getInt(
            self, "Path Value", "Enter Path Value:")

        if ok:
            self.le5.setText(str(num))

    def ex(self):
        global agent_starting_position, n, target, penalities, path_value, epsilon
        n = int(self.le.text()) if self.le.text() != "" else 15
        agent_starting_position = list(
            map(int, (str(self.le1.text())).split(","))) if self.le1.text() != "" else [5, 5]
        target = list(map(int, (str(self.le2.text())).split(","))
                      ) if self.le2.text() != "" else [10, 10]
        penalities = int((n*n*int(self.le3.text())/100)
                         ) if self.le3.text() != "" else 40
        epsilon = float(self.le4.text()) if self.le4.text() != "" else 0.3
        path_value = float(self.le5.text()) if self.le5.text() != "" else -0.1
        self.close()


def settingsWindow():
    app = QtWidgets.QApplication(sys.argv)
    ex = QLearningSettings()
    ex.show()
    app.exec_()


settingsWindow()


def settings():
    global reward, penalities, target, obstacles, agent_starting_position, n, path_value, Q, scrx, scry, csize

    scrx = n * csize
    scry = n * csize
    Q = np.zeros((n ** 2, 4))
    reward = np.zeros((n, n))
    reward[target[0], target[1]] = 5

    while penalities != 0:
        i = r(0, n - 1)
        j = r(0, n - 1)
        if reward[i, j] == 0 and [i, j] != agent_starting_position and [i, j] != target:
            reward[i, j] = -5
            penalities -= 1
            obstacles.append(n * i + j)

    obstacles.append(n * target[0] + target[1])

    for i in range(n):
        for j in range(n):
            if reward[i, j] == 0:
                reward[i, j] = path_value

    k = 0
    for i in range(n):
        for j in range(n):
            states[(i, j)] = k
            k += 1


cuda.jit()


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


cuda.jit()


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
            [i for i, a in enumerate(possible_actions)
             if a == max(possible_actions)]
        )
        return action


cuda.jit()


def episode():
    global current_pos, epsilon, agent_starting_position, temp, sumOfRewards, highestReward, highestReward_counter, shortest_path, episodeViaStep, step, repeatLimit
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
        Q[current_state, action] = reward[current_pos[0],
                                          current_pos[1]] + gamma * np.max(Q[new_state])
        temp += reward[current_pos[0], current_pos[1]]
        step += 1
        if highestReward_counter >= (repeatLimit*4/5):
            pos = [current_pos[0], current_pos[1]]
            shortest_path.append(pos)
    else:
        Q[current_state, action] = reward[current_pos[0],
                                          current_pos[1]] + gamma * np.max(Q[new_state])
        temp += reward[current_pos[0], current_pos[1]]
        if temp > highestReward:
            highestReward = temp
        if temp == highestReward:
            highestReward_counter += 1
        sumOfRewards.append(temp)
        episodeViaStep.append(step)
        step = 0
        temp = 0
        if highestReward_counter < repeatLimit:
            shortest_path = []
        current_pos = [agent_starting_position[0], agent_starting_position[1]]
        epsilon -= 1e-4


def draw_shortest_path():
    global n, shortest_path
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
            if [i, j] == agent_starting_position:
                pygame.draw.rect(
                    screen,
                    (25, 129, 230),
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

            if [i, j] in shortest_path:
                pygame.draw.rect(
                    screen,
                    colors[3],
                    (
                        (j * csize) + 3,
                        (i * csize) + 3,
                        (j * csize) + 11,
                        (i * csize) + 11,
                    ),
                    0,
                )

    pygame.display.flip()

    plt.subplot(1, 2, 1)
    plt.plot(sumOfRewards)
    plt.xlabel("Episodes")
    plt.ylabel("Episode via cost")

    plt.subplot(1, 2, 2)
    plt.plot(episodeViaStep)
    plt.xlabel("Episodes")
    plt.ylabel("Episode via step")
    plt.show()


def map2txt():
    global path_value
    f = open("engel.txt", "w")
    for i in range(n):
        for j in range(n):
            if reward[i, j] == -5:
                f.write("({}, {}, RED)\n".format(i, j))
            if reward[i, j] == 5:
                f.write("({}, {}, GREEN)\n".format(i, j))
            if reward[i, j] == path_value and [i, j] != agent_starting_position:
                f.write("({}, {}, GRAY)\n".format(i, j))
            if [i, j] == agent_starting_position:
                f.write("({}, {}, BLUE)\n".format(
                    agent_starting_position[0], agent_starting_position[1]))
    f.close()


current_pos = [agent_starting_position[0], agent_starting_position[1]]
settings()
screen = pygame.display.set_mode((scrx, scry))
map2txt()
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
        if event.type == pygame.KEYDOWN:
            plt.plot(sumOfRewards)
            plt.xlabel("Episodes")
            plt.ylabel("Episode via cost")
            plt.show()

    if highestReward_counter < repeatLimit:
        episode()
    else:
        map2txt()
        draw_shortest_path()

    pygame.display.flip()
