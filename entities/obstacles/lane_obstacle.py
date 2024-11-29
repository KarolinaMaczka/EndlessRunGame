from ursina import invoke

from config.constants import LANE_WIDTH, ROAD_WIDTH
from entities.obstacles.obstacle import Obstacle


class LaneObstacle(Obstacle):
    def __init__(self, models, position_z: float, difficulty: int, lane: int = 0, height: float = 0,
                 width: float = 0, depth: float = 0):
        super().__init__(models,position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)
        self.lane = lane

    @staticmethod
    def set_fixed_lane(obj, lane):
        obj.x = -ROAD_WIDTH / 2 + LANE_WIDTH / 2 + lane * LANE_WIDTH

    def set_lane(self, lane):
        self.lane = lane
        for child in self.children:
            invoke(self.set_fixed_lane, child, self.lane)

