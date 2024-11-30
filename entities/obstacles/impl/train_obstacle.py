from copy import copy

from ursina import Entity, color, invoke

from config.constants import LANE_WIDTH
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle


class ObstacleTrain(LaneObstacle):
    def __init__(self, models,position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.orange, height: float = 10,
                 width: float = LANE_WIDTH - 1, depth: float = 100):
        super().__init__(models, position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)

        self.body = Entity(
            model=copy(models.train),
            color=colorr,
            z=position_z,
            collider='box',
            double_sided=True,
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )
        self.body.texture_setter(copy(models.train_tex))

        self.children = [self.body]

        self.set_depth(depth)
        self.set_lane(lane)
        self.set_height(height)
        self.set_width(width)
        self.set_always_on_top()

    def set_width(self, width):
        self.width = width
        invoke(Obstacle.set_fixed_width, self.body, width)

    def set_height(self, height):
        self.height = height
        invoke(Obstacle.set_fixed_height, self.body, height)
        invoke(Obstacle.set_y_position, self.body)

    def set_depth(self, depth):
        self.depth = depth
        invoke(Obstacle.set_fixed_depth, self.body, depth)
