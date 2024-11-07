import random
from dataclasses import dataclass
from difficulty.maps.map import ObstacleMap


@dataclass
class ThirdObstacleMap(ObstacleMap):
    """
    signs: yes
    trains: yes,
    small obstacles: yes
    gates: yes
    small obstacles and trains are never at the same z position
    small obstacles are not next to each other
    """
    change_obstacle_type_cons: float = 0.5

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

            self._create_signs(z_position=last_obstacle_z - obstacle_generation_distance / 2)
            if random.random() < self.gate_generation_const:
                if obstacle_generation_distance <= 150:
                    last_obstacle_z += obstacle_generation_distance
                self._generate_gate(last_obstacle_z)
                if obstacle_generation_distance <= 150:
                    last_obstacle_z += obstacle_generation_distance
            elif random.random() < self.change_obstacle_type_cons:
                self._create_trains(start_x, last_obstacle_z)
            else:
                self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += obstacle_generation_distance
        return last_obstacle_z
