from CarlaEnv import CarlaEnv
import carla, threading, cv2


def main():
    weather = carla.WeatherParameters(
        cloudiness=0.0,
        precipitation=0.0,
        sun_altitude_angle=0.0)
    town = "Town02"
    environment = CarlaEnv(town, weather)
    blueprint_library: carla.BlueprintLibrary = environment.get_blueprint_library()

    while True:
        model = blueprint_library.filter("model3")[0]
        cam = blueprint_library.find("sensor.camera.rgb")
        colsensor = blueprint_library.find('sensor.other.collision')
        environment.spawn_vehicle(model, cam, colsensor)
        environment.show_image()
        '''collisions = threading.Thread(target=environment.reset)
        show_image = threading.Thread(target=environment.show_image)
        collisions.start()
        show_image.start()

        collisions.join()
        show_image.join()'''


if __name__ == '__main__':
    # main()
    image = cv2.imread("avatar.JPG")
    cv2.imshow("", image)
    if cv2.waitKey(0) == ord('q'):
        aux = False
