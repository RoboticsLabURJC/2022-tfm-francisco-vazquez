import glob, os, sys, carla, random, time


class CarlaEnv:
    def __init__(self, town, weather):
        self.im_width = 640
        self.im_height = 480
        self.client = carla.Client("localhost", 2000)
        self.client.load_world(town)
        self.client.set_timeout(20.0)
        self.world: carla.World = self.client.get_world()
        self.blueprint_library = self.world.get_blueprint_library()
        self.world.set_weather(weather)
        self.model3: carla.Vehicle = self.blueprint_library.filter("model3")[0]

    def reset(self):
        pass
