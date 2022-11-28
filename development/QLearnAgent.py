import carla
import cv2
import numpy as np
from CarlaEnv import CarlaEnv


class QLearnAgent:
    def __init__(self, agent: carla.Vehicle):
        self._agent: carla.Vehicle = agent
        self._state = [0] * 17

    def new_state(self, line_center):
        self._state = [0] * 17
        state = 0
        for i in range(17):
            if 38 * i < line_center < 38 * (i + 1):
                print(i)
                state = i

        self._state[state] = 1

        for i in range(-8, 9):
            if state == (i + 8):
                state = i

        print(state)
        print(self._state)
