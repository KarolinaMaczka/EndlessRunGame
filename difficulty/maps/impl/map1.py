import random
from dataclasses import dataclass, field
from typing import List

from config.constants import LANE_COUNT, Color
from difficulty.maps.map import ObstacleMap
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.gate_obstacle import ObstacleGate
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.train_obstacle import ObstacleTrain
from entities.obstacles.impl.wooden_sign_obstacle import ObstacleWoodenSign
from entities.obstacles.impl.indicator_obstacle import ObstacleIndicator
from entities.obstacles.obstacle_metadata_factory import ObstacleFactory


@dataclass
class FirstObstacleMap(ObstacleMap):
    """
    signs: yes
    trains: yes,
    small obstacles: yes
    gates: yes
    small obstacles and trains are always at the same z position
    small obstacles cannot be next to each other
    """
    def generate_obstacles(self, start, length):
        last_obstacle_z = start + self.obstacle_generation_distance
        last_obstacle_z = self._adjust_last_position(last_obstacle_z)
        end = start + length
        start_x = random.randint(0, 1)

        self.obstacles = []
        while last_obstacle_z <= end:
            if random.random() < self.lane_change_const:
                last_obstacle_z = self._adjust_last_position(last_obstacle_z)
                start_x = int(not start_x)

            self._create_signs(z_position=last_obstacle_z - self.obstacle_generation_distance / 2)
            if random.random() < self.gate_generation_const:
                last_obstacle_z = self._generate_gate(last_obstacle_z)
            else:
                self._create_trains(start_x, last_obstacle_z)
                self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += self.obstacle_generation_distance
        last_obstacle_z = self._adjust_last_position(last_obstacle_z)
        return last_obstacle_z

