import random
from abc import ABC, abstractmethod

from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.maps.map import ObstacleMap
from entities.obstacles.obstacle_metadata import ObstacleMetaData
from typing import Tuple, Any, Dict, List


class Difficulty(ABC):
    first_obstacle: float
    last_obstacle_z: float
    obstacle_generation_distance: int
    maps: list[ObstacleMap]

    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 obstacle_generation_distance=100, **kwargs):
        self.switch(first_obstacle, last_obstacle_z)
        self.obstacle_generation_distance = obstacle_generation_distance

    def switch(self, first_obstacle: float, last_obstacle_z: float):
        self.first_obstacle = first_obstacle
        self.last_obstacle_z = last_obstacle_z

    def generate_obstacle(self, player_z: float) -> tuple[Any, tuple[Any, Any, Any, Any, Any, Any, Any]] | tuple[
        list[Any], tuple[str, float, float, float, str, int]]:
        if player_z > self.first_obstacle + self.obstacle_generation_distance:
            spawn_z_position = self.last_obstacle_z + self.obstacle_generation_distance
            print(f"generating obstacles, z={player_z}, spawn.z = {spawn_z_position}")

            mapp = random.choice(self.maps)
            self.first_obstacle = self.last_obstacle_z
            self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance,
                                                           self.last_obstacle_z + 200, 2000)
            self.last_obstacle_z += self.obstacle_generation_distance
            return mapp.obstacles, self.__build_map_data(mapp, self.first_obstacle, self.last_obstacle_z)
        return [], ("", 0.0, 0.0, 0.0, "", 0, 0)

    def initialize_obstacles(self) -> tuple[Any, tuple[Any, Any, Any, Any, Any, Any, Any]]:
        mapp = random.choice(self.maps)
        self.last_obstacle_z = mapp.generate_obstacles(self.obstacle_generation_distance, self.first_obstacle,
                                                       INITIAL_LAST_OBSTACLE_Z_POS - INITIAL_FIRST_OBSTACLE_Z_POS - self.obstacle_generation_distance)
        self.last_obstacle_z += self.obstacle_generation_distance
        return mapp.obstacles, self.__build_map_data(mapp, INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS)

    def __build_map_data(self, mapp, first_obstacle=0.0, last_obstacle=0.0):
        return (type(mapp).__name__, mapp.lane_change_const, mapp.small_obstacle_const, mapp.gate_generation_const,
                mapp.color_theme.name, first_obstacle, last_obstacle)