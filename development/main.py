from CarlaEnv import CarlaEnv
import carla


def main():
    weather = carla.WeatherParameters(
        cloudiness=0.0,
        precipitation=0.0,
        sun_altitude_angle=0.0)
    town = "Town02"
    environment = CarlaEnv(town, weather)


if __name__ == '__main__':
    main()