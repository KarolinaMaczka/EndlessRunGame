import random

from ursina import invoke

from config.constants import CollisionType, CollisionSide, ROAD_WIDTH, LANE_WIDTH
from entities.obstacles.obstacle import Obstacle


class ObstacleSign(Obstacle):
    def __init__(self, models,position_z: float, difficulty: int, lane: int = 0, height: float = 0,
                 width: float = 0, depth: float = 0):
        super().__init__(models, position_z=position_z, difficulty=difficulty, lane=lane, height=height, width=width,
                         depth=depth)
        self.lane = lane

    @staticmethod
    def set_fixed_lane(obj, lane):
        obj.x = -ROAD_WIDTH / 2 + lane * LANE_WIDTH

    def set_lane(self, lane):
        self.lane = lane
        for child in self.children:
            invoke(self.set_fixed_lane, child, self.lane)

    def check_collision_type(self, *args, **kwargs) -> CollisionType:
        return CollisionType.LIGHT

    def check_collision_side(self, *args, **kwargs) -> CollisionSide:
        '''
        we randomly apply a side were we are going to bounce
        '''
        if random.random() < 0.5:
            collision_side = CollisionSide.LEFT
        else:
            collision_side = CollisionSide.RIGHT

        return collision_side
