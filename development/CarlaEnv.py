import carla
import cv2
import numpy as np


class CarlaEnv:
    def __init__(self, town, weather):
        self.im_width = 640
        self.im_height = 480
        self.client = carla.Client("localhost", 2000)
        self.client.load_world(town)
        self.client.set_timeout(20.0)
        self.world: carla.World = self.client.get_world()
        self.world.set_weather(weather)

        self._actors = []
        self._data_dict = {}
        self._collision_hist = []
        self._vehicle = None
        self._colsensor = None

        '''self._lowthresholds = (59.0, 28.0, 45.0)
        self._highthresholds = (64.0, 98.0, 75.0)'''

        self._lowthresholds = (0, 0, 0)
        self._highthresholds = (62, 255, 255)

    def control(self, action):
        if action == 0:
            self._vehicle.apply_control(carla.VehicleControl(throttle=0.6, steer=0))
        elif action == 1:
            self._vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.3))
        elif action == -1:
            self._vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=-0.3))

    '''def reset(self):
        while True:
            if len(self._actors) == 0:
                break
            elif len(self._collision_hist) > 0:
                for actor in self._actors:
                    actor.destroy()
                    self._collision_hist = []'''

    def spawn_vehicle(self, model: carla.BlueprintLibrary, camera=None, collision_detector=None):
        # spawn_point = carla.Transform(carla.Location(x=41.389999, y=275.029999, z=0.500000),
        # carla.Rotation(pitch=0.000000, yaw=89.999954, roll=0.000000))

        '''spawn_point = carla.Transform(carla.Location(x=71.965233, y=-10, z=0.300000),
                                      carla.Rotation(pitch=0.000000, yaw=-60.0, roll=0.000000))'''

        spawn_point = carla.Transform(carla.Location(x=71.7, y=-10, z=0.300000),
                                      carla.Rotation(pitch=0.000000, yaw=-62.5, roll=0.000000))
        '''for Location in self.world.get_map().get_spawn_points():
            print(Location)'''

        # print(f"Vehicle spawned at {spawn_point}")

        self._vehicle = self.world.spawn_actor(model, spawn_point)
        self._actors.append(self._vehicle)

        transform = carla.Transform(carla.Location(x=2.5, z=0.7))
        if camera is not None:
            camera.set_attribute("image_size_x", "640")
            camera.set_attribute("image_size_y", "480")
            camera.set_attribute("fov", "110")

            sensor = self.world.spawn_actor(camera, transform, attach_to=self._vehicle)
            self._actors.append(sensor)
            sensor.listen(lambda data: self._process_image(data))
        if collision_detector is not None:
            self._colsensor = self.world.spawn_actor(collision_detector, transform, attach_to=self._vehicle)
            self._actors.append(self._colsensor)
            self._colsensor.listen(lambda event: self._collision_data(event))

    def _process_image(self, data):
        """Convert a CARLA raw image to a BGRA numpy array."""
        if not isinstance(data, carla.Image):
            raise ValueError("Argument must be a carla.Image")
        image = np.array(data.raw_data)
        image2 = image.reshape((480, 640, 4))
        image3 = image2[:, :, :3]
        self._data_dict["image"] = image3

    def _collision_data(self, event):
        # self._collision_hist.append(event)
        if len(self._actors) > 0:
            self.destroy_all_actors()

        blueprint_library: carla.BlueprintLibrary = self.get_blueprint_library()
        model = blueprint_library.filter("model3")[0]
        cam = blueprint_library.find("sensor.camera.rgb")
        colsensor = blueprint_library.find('sensor.other.collision')
        self.spawn_vehicle(model, cam, colsensor)
        # self.control(carla.VehicleControl(throttle=1, steer=0))

    def get_blueprint_library(self):
        return self.world.get_blueprint_library()

    def show_image(self):
        if len(self._data_dict) > 0:
            cv2.imshow("image", self._data_dict["image"])
            if cv2.waitKey(1) == ord('q'):
                return False
        else:
            print("There is no image to show.")

        return True

    def calc_center(self):
        open_cv_image = np.uint8(self._data_dict["image"])
        open_cv_image = open_cv_image[240:480, :, :]
        image_copy = np.copy(open_cv_image)

        hsv_frame = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_frame, self._lowthresholds, self._highthresholds)

        x = 630
        while x > 0:
            if mask[100][x] == 255:
                break
            x -= 1

        z = x
        while z > 0:
            if mask[100][z] != 255:
                break
            z -= 1

        cv2.circle(mask, (x, 100), 2, (0, 255, 0), -1)
        cv2.circle(mask, (z, 100), 2, (0, 255, 0), -1)

        # Calc distance from center of the image to center of the lane
        distance = ((x + z) / 2) - 320
        pos = ((x + z) / 2)

        return pos

    def destroy_all_actors(self):
        for actor in self._actors:
            actor.destroy()
        self._actors = []
