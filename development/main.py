import time
import carla
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

    aux = True
    while aux:
        aux = environment.show_image()
        action = carla.VehicleControl(throttle=0.6, steer=0)
        agent.step(0)
        pos = environment.calc_center()
        reward = agent.reward(action, pos)
        print(reward)
        # agent.new_state(pos)

    environment.destroy_all_actors()


if __name__ == '__main__':
    main()
