from CarlaEnv import CarlaEnv
import carla


def main():
    weather = carla.WeatherParameters(
        cloudiness=0.0,
        precipitation=0.0,
        sun_altitude_angle=0.0)
    town = "Town02"
    environment = CarlaEnv(town, weather)
    blueprint_library: carla.BlueprintLibrary = environment.get_blueprint_library()

    model = blueprint_library.filter("model3")[0]
    cam = blueprint_library.find("sensor.camera.rgb")
    colsensor = blueprint_library.find('sensor.other.collision')
    environment.spawn_vehicle(model, cam, colsensor)
    environment.step(None)
    aux = False
    while not aux:
        aux = environment.reset()


if __name__ == '__main__':
    main()