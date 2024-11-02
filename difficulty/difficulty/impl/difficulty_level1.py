import random

from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.maps.color_themes import COLOR_THEME_COLORFULL
from difficulty.maps.impl.map1 import FirstObstacleMap
from difficulty.maps.impl.map2 import SecondObstacleMap
from difficulty.maps.impl.map3 import ThirdObstacleMap
from difficulty.maps.impl.map4 import FourthObstacleMap
from difficulty.maps.impl.map5 import FifthObstacleMap
from difficulty.maps.impl.map6 import SixthObstacleMap
from entities.obstacles.obstacle_metadata import ObstacleMetaData


class Difficulty1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, 100, **kwargs)
        self.maps = [FirstObstacleMap(lane_change_const=0.1, small_obstacle_const=0.2, gate_generation_const=0.2),
                     FirstObstacleMap(lane_change_const=0.25, small_obstacle_const=0.3, gate_generation_const=0.2, color_theme=COLOR_THEME_COLORFULL),
                     SecondObstacleMap(lane_change_const=0.25, small_obstacle_const=0.4, gate_generation_const=0.4),
                     ThirdObstacleMap(lane_change_const=0.5, small_obstacle_const=1, gate_generation_const=0.1),
                     FourthObstacleMap(lane_change_const=0.25, small_obstacle_const=1, gate_generation_const=0.2),
                     FifthObstacleMap(small_obstacle_const=1, gate_generation_const=0.1),
                     SixthObstacleMap(small_obstacle_const=1, gate_generation_const=0.2)
                     ]

    def generate_obstacle(self, player_z: float) -> list[ObstacleMetaData]:
        if player_z > self.first_obstacle + self.obstacle_generation_distance:
            spawn_z_position = self.last_obstacle_z + self.obstacle_generation_distance
            print(f"generating obstacles, z={player_z}, spawn.z = {spawn_z_position}")

            mapp = random.choice(self.maps)
            self.first_obstacle = self.last_obstacle_z
            self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance, self.last_obstacle_z, 2000)
            return mapp.obstacles

    def initialize_obstacles(self) -> list[ObstacleMetaData] :
        mapp = random.choice(self.maps)
        self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance, self.first_obstacle, INITIAL_LAST_OBSTACLE_Z_POS - INITIAL_FIRST_OBSTACLE_Z_POS)
        self.last_obstacle_z += self.obstacle_generation_distance
        return mapp.obstacles
