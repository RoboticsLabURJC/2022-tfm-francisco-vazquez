import random
import carla
import cv2
import numpy as np


class QLearnAgent:
    def __init__(self, env):
        self._env = env
        self.state = [0] * 3
        self._actions = [0, 1, 2]
        self.Q_table = {} # np.zeros([17**3, 3])

        for i in range(17):
            for j in range(17):
                for k in range(17):
                    aux = (i, j, k)
                    action_reward = (0, 0, 0)
                    self.Q_table[aux] = action_reward

    def new_state(self, line_centers):
        for p in range(len(line_centers)):
            for i in range(17):
                if 38 * i <= line_centers[p] < 38 * (i + 1):
                    self.state[p] = i

        '''to_print = 0
        for i in range(-8, 9):
            if self.state == (i + 8):
                to_print = i
        # print(f"Real state: {to_print}")'''
        '''print(f"Estado actual: {state}", end=f" representado como: {self._state}")
        print()
        print()'''

        return self.state

    def step(self, action):
        if action in self._actions:
            self._env.control(action)
            positions = self._env.calc_center()
            new_state = self.new_state(positions)
            reward = self.reward()
            done = False
            info = None

            if reward == -100:  # or self._env.getcollision:
                # print(self._env.getcollision)
                done = True
                print(f"Reward: {reward}, state: {new_state}, done: {done}, position of the center: {pos}")

            return new_state, reward, done, info

    def reset(self):
        self._env.reset()
        pos = self._env.calc_center()
        new_state = self.new_state(pos)
        return new_state

    def reward(self):
        reward = 0
        for state in self.state:
            if 7 <= state <= 9:
                reward += 10

            elif state in [5, 6, 10, 11]:
                reward += 2

            elif state in [2, 3, 4, 12, 13, 14]:
                reward += 1

            else:
                return -100
        return reward

    def get_action(self):
        return random.choice(self._actions)
