import copy

from entities.obstacles.obstacle_metadata import ObstacleMetaData
import random


class ObstacleFactory:
    _obstacles: list[ObstacleMetaData]

    def __init__(self, init_lane_obstacles: list[dict], lanes: int):
        self._obstacles = []
        self.lanes = lanes
        for obstacle_type in init_lane_obstacles:
            self._obstacles.append(ObstacleMetaData(**obstacle_type))

    def get_random(self):
        total_weight = sum(item.probability[0] for item in self._obstacles)
        rand = random.uniform(0, total_weight)
        cumulative_weight = 0

        for item in self._obstacles:
            cumulative_weight += item.probability[0]
            if rand < cumulative_weight:
                return item

    def create_obstacle(self, position_z: float, lane: int) -> ObstacleMetaData:
        obstacle_type = self.get_random()
        obstacle_type.position_z = position_z
        obstacle_type.lane = lane
        return copy.copy(obstacle_type)

