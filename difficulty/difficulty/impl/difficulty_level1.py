import random
from typing import Tuple, Any, Dict, List

from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.maps.color_themes import ColorTheme
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
        self.maps = [
            FirstObstacleMap(lane_change_const=0.1, small_obstacle_const=0.2, gate_generation_const=0.2),
            FirstObstacleMap(lane_change_const=0.25, small_obstacle_const=0.3, gate_generation_const=0.2,
                             color_theme=ColorTheme.COLOR_THEME_BASIC),
            SecondObstacleMap(lane_change_const=0.25, small_obstacle_const=0.4, gate_generation_const=0.4),
            ThirdObstacleMap(lane_change_const=0.5, small_obstacle_const=1, gate_generation_const=0.1),
            FourthObstacleMap(lane_change_const=0.25, small_obstacle_const=1, gate_generation_const=0.2),
            FifthObstacleMap(small_obstacle_const=1, gate_generation_const=0.1),
            SixthObstacleMap(small_obstacle_const=1, gate_generation_const=0.2)
        ]

    # def generate_obstacle(self, player_z: float) -> tuple[Any, tuple[Any, Any, Any, Any, Any, Any, Any]] | tuple[
    #     list[Any], tuple[str, float, float, float, str, int]]:
    #     if player_z > self.first_obstacle + self.obstacle_generation_distance:
    #         spawn_z_position = self.last_obstacle_z + self.obstacle_generation_distance
    #         print(f"generating obstacles, z={player_z}, spawn.z = {spawn_z_position}")
    #
    #         mapp = random.choice(self.maps)
    #         self.first_obstacle = self.last_obstacle_z
    #         self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance,
    #                                                        self.last_obstacle_z + 200, 2000)
    #         self.last_obstacle_z += self.obstacle_generation_distance
    #         return mapp.obstacles, self.__build_map_data(mapp, self.first_obstacle, self.last_obstacle_z)
    #     return [], ("", 0.0, 0.0, 0.0, "", 0, 0)
    #
    # def initialize_obstacles(self) -> tuple[Any, tuple[Any, Any, Any, Any, Any, Any, Any]]:
    #     mapp = random.choice(self.maps)
    #     self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance, self.first_obstacle,
    #                                                    INITIAL_LAST_OBSTACLE_Z_POS - INITIAL_FIRST_OBSTACLE_Z_POS - self.obstacle_generation_distance)
    #     self.last_obstacle_z += self.obstacle_generation_distance
    #     return mapp.obstacles, self.__build_map_data(mapp, INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS)
    #
    # def __build_map_data(self, mapp, first_obstacle=0.0, last_obstacle=0.0):
    #     return (type(mapp).__name__, mapp.lane_change_const, mapp.small_obstacle_const, mapp.gate_generation_const,
    #     mapp.color_theme.name, first_obstacle, last_obstacle)
