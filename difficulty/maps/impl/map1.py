import random
from dataclasses import dataclass, field
from typing import List

from difficulty.maps.map import ObstacleMap


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
                self._create_trains(start_x, last_obstacle_z, self.big_obstacle_const)
                self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += self.obstacle_generation_distance
        last_obstacle_z = self._adjust_last_position(last_obstacle_z)
        return last_obstacle_z

