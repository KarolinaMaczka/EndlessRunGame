import random
from dataclasses import dataclass

from config.constants import LANE_COUNT
from difficulty.maps.impl.map5 import FifthObstacleMap

@dataclass
class SixthObstacleMap(FifthObstacleMap):
    """
    signs: yes
    trains: no,
    small obstacles: yes
    gates: yes
    small obstacles can be next to each other
    """
    def _create_small_obstacles(self, start_x: int, z_position: float, small_obstacle_const):
        for lane in range(start_x, LANE_COUNT):
            if random.random() < small_obstacle_const:
                self.obstacles.append(self._small_obstacles.create_obstacle(z_position, lane))