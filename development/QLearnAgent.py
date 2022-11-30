import random
import carla
import cv2
import numpy as np


class QLearnAgent:
    def __init__(self, env):
        self._env = env
        self._state = [0] * 17
        self._actions = [0, 1, 2]
        self.Q_table = np.zeros([17, 3])

    def new_state(self, line_center):
        self._state = [0] * 17
        state = 0
        for i in range(17):
            if 38 * i <= line_center <= 38 * (i + 1):
                state = i

        self._state[state] = 1

        to_print = 0
        for i in range(-8, 9):
            if state == (i + 8):
                to_print = i
        # print(f"Real state: {to_print}")
        '''print(f"Estado actual: {state}", end=f" representado como: {self._state}")
        print()
        print()'''

        return state

    def step(self, action):
        if action in self._actions:
            self._env.control(action)
            pos = self._env.calc_center()
            new_state = self.new_state(pos)
            reward = self.reward()
            done = False
            info = None

            if reward == -100:  # or self._env.getcollision:
                # print(self._env.getcollision)
                done = True
                # print(f"Reward: {reward}, state: {new_state}, done: {done}, position of the center: {pos}")

            return new_state, reward, done, info

    def reset(self):
        self._env.reset()
        pos = self._env.calc_center()
        new_state = self.new_state(pos)
        return new_state

    def reward(self):
        state = np.argmax(self._state)

        if 7 <= state <= 9:
            return 10

        elif state in [5, 6, 10, 11]:
            return 2

        elif state in [2, 3, 4, 12, 13, 14]:
            return -10

        else:
            return -100

    def get_action(self):
        return random.choice(self._actions)
