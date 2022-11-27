import time
import carla
from CarlaEnv import CarlaEnv


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
    time.sleep(5)
    environment.step(carla.VehicleControl(throttle=1, steer=0))

    aux = True
    while aux:
        aux = environment.show_image()

        '''collisions = threading.Thread(target=environment.reset)
        show_image = threading.Thread(target=environment.show_image)
        collisions.start()
        show_image.start()

        collisions.join()
        show_image.join()'''

    environment.destroy_all_actors()


if __name__ == '__main__':
    main()
