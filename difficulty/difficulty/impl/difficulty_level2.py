import random

from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.maps.impl.map1 import FirstObstacleMap
from difficulty.maps.impl.map2 import SecondObstacleMap


class Difficulty2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, 100, **kwargs)
        self.maps = [SecondObstacleMap(lane_change_const=0.1, small_obstacle_const=0.5)]

    def generate_obstacle(self, player_z):
        if player_z > self.first_obstacle + self.obstacle_generation_distance:
            spawn_z_position = self.last_obstacle_z + self.obstacle_generation_distance
            print(f"generating obstacles, z={player_z}, spawn.z = {spawn_z_position}")

            self.last_obstacle_z += self.obstacle_generation_distance
            mapp = random.choice(self.maps)
            self.first_obstacle = self.last_obstacle_z
            self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance, self.last_obstacle_z,
                                                           2000)
            return mapp.obstacles

    def initialize_obstacles(self):
        mapp = random.choice(self.maps)
        self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance, self.first_obstacle,
                                                       INITIAL_LAST_OBSTACLE_Z_POS - INITIAL_FIRST_OBSTACLE_Z_POS - self.obstacle_generation_distance)
        return mapp.obstacles
