import random
from dataclasses import dataclass, field

from config.constants import LANE_COUNT
from difficulty.maps.impl.map1 import FirstObstacleMap
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.train_obstacle import ObstacleTrain
from entities.obstacles.obstacle_metadata_factory import ObstacleMetadataFactory


@dataclass
class SeventhObstacleMap(FirstObstacleMap):
    """
    signs: yes
    trains: yes,
    small obstacles: yes
    gates: yes
    small obstacles and trains are always at the same z position
    Train are next to each other
    Use only when generation distance is at least 300
    small obstacles cannot be next to each other
    """
    _big_obstacles: ObstacleMetadataFactory = field(default_factory=lambda: ObstacleMetadataFactory([
        {"obstacle": ObstacleLongCube, 'difficulty': 1, 'probability': 0.5, "has_ladder": 0.4},
        {"obstacle": ObstacleTrain, 'difficulty': 1, 'probability': 0.5}],
        4))
    def _create_trains(self, start_x: int, z_position: float):
        for lane in range(start_x, LANE_COUNT - (1 - start_x)):
            if random.random() < self.big_obstacle_const:
                self.obstacles.append(self._big_obstacles.create_obstacle(z_position, lane))
            elif random.random() < self.small_obstacle_const:
                self.obstacles.append(self._small_obstacles.create_obstacle(z_position, lane))

    def _create_small_obstacles(self, start_x: int, z_position: float, small_obstacle_const):
        lane = 2 if start_x else 0
        if random.random() < small_obstacle_const:
            self.obstacles.append(self._small_obstacles.create_obstacle(z_position, lane))