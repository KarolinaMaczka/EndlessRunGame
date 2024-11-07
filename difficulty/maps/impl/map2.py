import random
from dataclasses import dataclass
from difficulty.maps.map import ObstacleMap

@dataclass
class SecondObstacleMap(ObstacleMap):
    """
    signs: no
    trains: yes,
    small obstacles: yes
    gates: yes
    small obstacles and trains are always at the same z position
    small obstacles cannot be next to each other
    """

    def generate_obstacles(self, obstacle_generation_distance, start, length):
        last_obstacle_z = start + obstacle_generation_distance
        end = start + length
        start_x = random.randint(0, 1)

        self.obstacles = []
        while last_obstacle_z <= end:
            if random.random() < self.lane_change_const:
                if obstacle_generation_distance <= 150:
                    last_obstacle_z += obstacle_generation_distance

                start_x = int(not start_x)

            if random.random() < self.gate_generation_const:
                if obstacle_generation_distance <= 150:
                    last_obstacle_z += obstacle_generation_distance
                self._generate_gate(last_obstacle_z)
                if obstacle_generation_distance <= 150:
                    last_obstacle_z += obstacle_generation_distance
            else:
                self._create_trains(start_x, last_obstacle_z)
                self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += obstacle_generation_distance
        return last_obstacle_z
