import glob
import os
import sys
import cv2
import numpy as np
from LineDetector import LineDetector
import carla

try:
    sys.path.append(
        glob.glob('/home/xfranv8/Documents/CARLA 0.9.13/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (  # PREGUNTAR!!
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


def procces_image(data, data_dict):
    """Convert a CARLA raw image to a BGRA numpy array."""
    if not isinstance(data, carla.Image):
        raise ValueError("Argument must be a carla.Image")
    image = np.array(data.raw_data)
    image2 = image.reshape((480, 640, 4))
    # image3 = image2[:, :, :3]
    data_dict['image'] = image2

    # return image2 / 255.0


actor_list = []
client = carla.Client("localhost", 2000)
client.load_world("Town02")
client.set_timeout(20.0)
world: carla.World = client.get_world()
blueprint_library: carla.BlueprintLibrary = world.get_blueprint_library()
weather = carla.WeatherParameters(
    cloudiness=0.0,
    precipitation=0.0,
    sun_altitude_angle=0.0)
world.set_weather(weather)

bp = blueprint_library.filter("model3")[0]

# transform = carla.Transform(carla.Location(x=230, y=195, z=40), carla.Rotation(yaw=180))
spawn_point = carla.Transform(carla.Location(x=41.389999, y=275.029999, z=0.500000),
                              carla.Rotation(pitch=0.000000, yaw=89.999954, roll=0.000000))
vehicle: carla.Vehicle = world.spawn_actor(bp, spawn_point)

# vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))
actor_list.append(vehicle)

cam_bp = blueprint_library.find("sensor.camera.rgb")
cam_bp.set_attribute("image_size_x", "640")
cam_bp.set_attribute("image_size_y", "480")
cam_bp.set_attribute("fov", "110")
# cam_bp.set_attribute('sensor_tick', '0.1')

spawn_pont = carla.Transform(carla.Location(x=2.5, z=0.7))
sensor = world.spawn_actor(cam_bp, spawn_pont, attach_to=vehicle)
actor_list.append(sensor)
camera_data = {"image": np.zeros((480, 640, 4))}
sensor.listen(lambda data: procces_image(data, camera_data))

vehicle.apply_control(carla.VehicleControl(throttle=0.4, steer=0))
# vehicle.set_autopilot(True)

detector = LineDetector()
cv2.namedWindow("CAR VIEW")  # Create a named window
cv2.moveWindow("CAR VIEW", 1958, 0)
while True:

    open_cv_image = np.uint8(camera_data["image"])
    imcopy = np.copy(open_cv_image)
    cv2.line(imcopy, (320, 480), (320, 0), (0, 0, 255), 2)
    # cv2.imshow("RGB Camera", open_cv_image)
    x1, y1, x2, y2 = detector.detect_points(open_cv_image)

    # cv2.imshow("Morphological Transforms", image)
    if x1 is not None:
        cv2.circle(imcopy, (x1, y1), 3, (255, 0, 0), 1)
    if x2 is not None:
        cv2.circle(imcopy, (x2, y2), 3, (255, 0, 0), 1)

    if x2 is None and x1 is not None:
        aux = 340 - (680 - x1) - 40
        x2, y2 = aux, y1
        cv2.circle(imcopy, (x2, y2), 3, (255, 0, 0), 1)
    elif x1 is None and x2 is not None:
        x1, y1 = 640, y2
    elif x1 is None and x2 is None:
        cv2.line(imcopy, (320, 480), (620, 400), (0, 255, 0), 2)
        vehicle.apply_control(carla.VehicleControl(throttle=0, steer=0.7))
    if x2 is not None and x1 is not None:
        pmx = int((x2 + x1) / 2)
        pmy = int((y2 + y1) / 2)
        steer = (pmx - 340) * 0.002

        cv2.line(imcopy, (320, 480), (pmx, pmy), (0, 255, 0), 2)
        vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=steer))

    cv2.imshow("CAR VIEW", imcopy)
    if cv2.waitKey(1) == ord('q'):
        break

vehicle.disable_constant_velocity()
cv2.destroyAllWindows()

for actor in actor_list:
    actor.destroy()
