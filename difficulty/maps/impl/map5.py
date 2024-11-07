import random
from dataclasses import dataclass, field
from difficulty.maps.map import ObstacleMap
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.obstacle_metadata_factory import ObstacleFactory


@dataclass
class FifthObstacleMap(ObstacleMap):
    """
    signs: yes
    trains: no,
    small obstacles: yes
    gates: yes
    small obstacles are not next to each other
    """

    _small_obstacles: ObstacleFactory = field(default_factory=lambda: ObstacleFactory([
        {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.3},
        {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.4},
        {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.2},
        {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.1}],
        4))

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
            else:
                self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += obstacle_generation_distance
        return last_obstacle_z