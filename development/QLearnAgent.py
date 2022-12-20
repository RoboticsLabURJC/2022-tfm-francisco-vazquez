import random
import time

import carla
import cv2
import numpy as np


class QLearnAgent:
    def __init__(self, env):
        self._env = env
        self.state = (0, 0, 0)
        self._actions = [0, 1, 2]
        self.Q_table = {} # np.zeros([17**3, 3])

        for i in range(17):
            for j in range(17):
                for k in range(17):
                    aux = (i, j, k)
                    action_reward = {}
                    for a in range(len(self._actions)):
                        action_reward[a] = 0
                    self.Q_table[aux] = action_reward

    def new_state(self, line_centers):
        aux = [0] * 3
        for p in range(len(line_centers)):
            for i in range(17):
                if 38 * i <= line_centers[p] < 38 * (i + 1):
                    aux[p] = i
                    self.state = tuple(aux)

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
            reward = self.reward(positions)
            done = False
            info = None

            if reward == 1e-3:  # or self._env.getcollision:
                # print(self._env.getcollision)
                done = True
                print(f"Reward: {reward}, state: {new_state}, done: {done}, position of the center: {positions}")

            print(f"Positions: {positions}")
            return new_state, reward, done, info

    def reset(self):
        self._env.reset()
        time.sleep(1)
        pos = self._env.calc_center()
        new_state = self.new_state(pos)
        return new_state

    def reward(self, positions):
        rewards = []


        distances = []
        for p in positions:
            distance = abs(320 - p)
            if distance <= 0.0:
                reward = 1
            elif distance <= 5.0:
                reward = 0.9
            elif distance <= 7.5:
                reward = 0.85
            elif distance <= 12.5:
                reward = 0.8
            elif distance <= 15.0:
                reward = 0.75
            elif distance <= 22.5:
                reward = 0.7
            elif distance <= 30.0:
                reward = 0.65
            elif distance <= 35.0:
                reward = 0.6
            elif distance <= 40.0:
                reward = 0.55
            elif distance <= 45.0:
                reward = 0.5
            elif distance <= 50.0:
                reward = 0.4
            elif distance <= 55.0:
                reward = 0.3
            elif distance <= 60.0:
                reward = 0.2
            elif distance <= 65.0:
                reward = 0.1
            else:
                reward = 1e-3

            rewards.append(reward)

        reward = 0.5 * rewards[0] + 0.3 * rewards[1] + 0.2 * rewards[2]
        return reward

    def get_action(self):
        return random.choice(self._actions)









