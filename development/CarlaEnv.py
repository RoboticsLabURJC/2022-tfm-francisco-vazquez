import glob, os, sys, carla, random, time, numpy as np


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
        self._vehicle: carla.Vehicle

    def step(self, action):
        self._vehicle.apply_control(carla.VehicleControl(throttle=1, steer=0))

    def reset(self):
        if len(self._collision_hist) > 0:
            for actor in self._actors:
                actor.destroy()
                self._collision_hist = []
                return True
        return False

    def spawn_vehicle(self, model: carla.BlueprintLibrary, camera=None, collision_detector=None):
        # spawn_point = carla.Transform(carla.Location(x=41.389999, y=275.029999, z=0.500000),
        # carla.Rotation(pitch=0.000000, yaw=89.999954, roll=0.000000))

        spawn_point = random.choice(self.world.get_map().get_spawn_points())

        self._vehicle = self.world.spawn_actor(model, spawn_point)
        self._actors.append(self._vehicle)

        transform = carla.Transform(carla.Location(x=2.5, z=0.7))
        if camera is not None:
            camera.set_attribute("image_size_x", "640")
            camera.set_attribute("image_size_y", "480")
            camera.set_attribute("fov", "110")

            sensor = self.world.spawn_actor(camera, transform, attach_to=self._vehicle)
            self._actors.append(sensor)
            camera_data = {"image": np.zeros((480, 640, 4))}
            sensor.listen(lambda data: self._process_image(data))
        if collision_detector is not None:
            colsensor = self.world.get_blueprint_library().find('sensor.other.collision')
            self.colsensor = self.world.spawn_actor(collision_detector, transform, attach_to=self._vehicle)
            self._actors.append(self.colsensor)
            self.colsensor.listen(lambda event: self._collision_data(event))

    def get_blueprint_library(self):
        return self.world.get_blueprint_library()

    def _process_image(self, data):
        """Convert a CARLA raw image to a BGRA numpy array."""
        if not isinstance(data, carla.Image):
            raise ValueError("Argument must be a carla.Image")
        image = np.array(data.raw_data)
        image2 = image.reshape((480, 640, 4))
        # image3 = image2[:, :, :3]
        self._data_dict['image'] = image2

    def _collision_data(self, event):
        self._collision_hist.append(event)
