import time
import carla
import random

import numpy as np

from CarlaEnv import CarlaEnv
from QLearnAgent import QLearnAgent


def main():
    weather = carla.WeatherParameters(
        cloudiness=0.0,
        precipitation=0.0,
        sun_altitude_angle=2.5)
    town = "Town07"
    environment = CarlaEnv(town, weather)

    blueprint_library: carla.BlueprintLibrary = environment.get_blueprint_library()

    model = blueprint_library.filter("model3")[0]
    cam = blueprint_library.find("sensor.camera.rgb")
    colsensor = blueprint_library.find('sensor.other.collision')
    environment.spawn_vehicle(model, cam, colsensor)

    agent = QLearnAgent(environment)
    time.sleep(5)

    '''aux = True
    while aux:
        aux = environment.show_image()
        action = carla.VehicleControl(throttle=0.6, steer=0)
        agent.step(0)
        pos = environment.calc_center()
        reward = agent.reward(action, pos)
        print(reward)
        # agent.new_state(pos)'''

    alpha = 0.8
    gamma = 0.9
    epsilon = 0.99

    for i in range(1, 10000, 1):
        state = agent.reset()
        time.sleep(1)

        epochs, penalties, reward = 0, 0, 0
        done = False

        while not done:
            '''if not environment.show_image():
                environment.destroy_all_actors()
                exit(0)'''
            if random.uniform(0, 1) < epsilon:
                action = agent.get_action()
                epsilon *= 0.998
            else:
                action = np.argmax(agent.Q_table[state])

            next_state, reward, done, info = agent.step(action)

            old_value = agent.Q_table[state, action]
            next_max = np.max(agent.Q_table[next_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            agent.Q_table[state, action] = new_value

            state = next_state
            epochs += 1

        print(f"Episode: {i}, elpsilon: {epsilon}")

    environment.destroy_all_actors()


if __name__ == '__main__':
    main()
