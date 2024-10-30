import random
from abc import ABC, abstractmethod

from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.maps.impl.map1 import FirstObstacleMap
from entities.obstacles.obstacle_metadata import ObstacleMetaData


class Difficulty(ABC):
    first_obstacle: float
    last_obstacle_z: float
    obstacle_generation_distance: int
    maps: list[FirstObstacleMap]

    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 obstacle_generation_distance=100, **kwargs):
        self.switch(first_obstacle, last_obstacle_z)
        self.obstacle_generation_distance = obstacle_generation_distance

    def switch(self, first_obstacle: float, last_obstacle_z: float):
        self.first_obstacle = first_obstacle
        self.last_obstacle_z = last_obstacle_z

    @abstractmethod
    def generate_obstacle(self, player_z: float) -> list[ObstacleMetaData]:
        pass

    @abstractmethod
    def initialize_obstacles(self) -> list[ObstacleMetaData]:
        pass
