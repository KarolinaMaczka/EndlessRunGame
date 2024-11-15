import copy

from config.logger import get_game_logger
from entities.obstacles.obstacle_metadata import ObstacleMetaData
import random
logger = get_game_logger()


class ObstacleFactory:
    _obstacles: list[ObstacleMetaData]

    def __init__(self, init_lane_obstacles: list[dict], lanes: int):
        self._obstacles = []
        self.lanes = lanes
        for obstacle_type in init_lane_obstacles:
            self._obstacles.append(ObstacleMetaData(**obstacle_type))

    def get_obstacles(self):
        return self._obstacles

    def apply_color_palette(self, palette):
        for obstacle in self._obstacles:
            if str(obstacle.obstacle.__name__) in palette.keys():
                obstacle.entity_metadata['colorr'] = palette[str(obstacle.obstacle.__name__)]

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
        # logger.info(f"Drawed by lot {type(obstacle_type.obstacle).__name__}")
        return copy.copy(obstacle_type)

