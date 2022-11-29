import carla
import cv2
import numpy as np
from CarlaEnv import CarlaEnv


class QLearnAgent:
    def __init__(self, env):
        self._env = env
        self._agent: carla.Vehicle = env._vehicle
        self._state = [0] * 17

    def new_state(self, line_center):
        self._state = [0] * 17
        state = 0
        for i in range(17):
            if 38 * i < line_center < 38 * (i + 1):
                state = i

        self._state[state] = 1

        for i in range(-8, 9):
            if state == (i + 8):
                state = i

        print(f"Estado actual: {state}", end=f" representado como: {self._state}")
        print()
        print()

    def step(self, action):
        if action in [0, 1, 2]:
            self._env.control(action)

    def reward(self, step, pos):
        self.new_state(pos)
        state = np.argmax(self._state)

        if 7 <= state <= 9:
            return 10

        elif state in [5, 6, 10, 11]:
            return 2

        elif state in [2, 3, 4, 12, 13, 14]:
            return 1

        else:
            return -100
