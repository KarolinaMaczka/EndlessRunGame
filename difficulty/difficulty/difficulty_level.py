import random
from abc import ABC, abstractmethod

from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.maps.map import ObstacleMap, MapMetadata
from entities.obstacles.obstacle_metadata import ObstacleMetaData
from typing import Tuple, Any, Dict, List

class Difficulty(ABC):
    first_obstacle: float
    last_obstacle_z: float
    maps: list[ObstacleMap]

    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.switch(first_obstacle, last_obstacle_z)

    def switch(self, first_obstacle: float, last_obstacle_z: float):
        self.first_obstacle = first_obstacle
        self.last_obstacle_z = last_obstacle_z

    def generate_obstacle(self, player_z: float) -> tuple[Any, MapMetadata] | tuple[list[Any], None]:
        if player_z > self.first_obstacle + 150:
            spawn_z_position = self.last_obstacle_z
            print(f"generating obstacles, z={player_z}, spawn.z = {spawn_z_position}")

            mapp = random.choice(self.maps)
            self.first_obstacle = self.last_obstacle_z
            self.last_obstacle_z = mapp.generate_obstacles(self.last_obstacle_z, 2000)
            return mapp.obstacles, mapp.get_metadata(self.first_obstacle, self.last_obstacle_z)
        return [], None

    def initialize_obstacles(self) -> tuple[Any, MapMetadata]:
        mapp = random.choice(self.maps)
        self.last_obstacle_z = mapp.generate_obstacles(self.first_obstacle,
                                                       INITIAL_LAST_OBSTACLE_Z_POS - INITIAL_FIRST_OBSTACLE_Z_POS)
        return mapp.obstacles, mapp.get_metadata(self.first_obstacle, self.last_obstacle_z)
