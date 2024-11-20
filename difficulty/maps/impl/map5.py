import random
from dataclasses import dataclass, field
from difficulty.maps.map import ObstacleMap
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.obstacle_metadata_factory import ObstacleMetadataFactory


@dataclass
class FifthObstacleMap(ObstacleMap):
    """
    signs: yes
    trains: no,
    small obstacles: yes
    gates: yes
    small obstacles are not next to each other
    """

    _small_obstacles: ObstacleMetadataFactory = field(default_factory=lambda: ObstacleMetadataFactory([
        {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.3},
        {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.4},
        {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.2},
        {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.1}],
        4))

    def generate_obstacles(self, start, length):
        last_obstacle_z = start + self.obstacle_generation_distance
        last_obstacle_z = self._adjust_last_position(last_obstacle_z)
        end = start + length
        start_x = random.randint(0, 1)

        self.obstacles = []
        while last_obstacle_z <= end+100:
            if random.random() < self.lane_change_const:
                last_obstacle_z = self._adjust_last_position(last_obstacle_z)
                start_x = int(not start_x)

            self._create_signs(z_position=last_obstacle_z - self.obstacle_generation_distance / 2)
            if random.random() < self.gate_generation_const:
                last_obstacle_z = self._generate_gate(last_obstacle_z)
            else:
                self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += self.obstacle_generation_distance
        last_obstacle_z = self._adjust_last_position(last_obstacle_z)
        return last_obstacle_z