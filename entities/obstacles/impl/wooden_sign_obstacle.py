from copy import copy

from ursina import color, Entity, invoke
from config.constants import STANDARD_OBSTACLE_HEIGHT
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.sign_obstacle import ObstacleSign


class ObstacleWoodenSign(ObstacleSign):
    def __init__(self, models, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.brown, height: float = STANDARD_OBSTACLE_HEIGHT-3,
                 width: float = 2, depth: float = 1):
        super().__init__(models,position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)

        self.body = Entity(
            model=copy(models.wood_sign),
            rotation=(0, 0, 0),
            color=colorr,
            z=position_z,
            collider='box',
            double_sided=True,
            jump=False,
            climb=False,
            sign=True,
            parentt=self
        )
        self.body.texture_setter(copy(models.wood_sign_tex))
        self.children = [self.body]
        self.set_height(height)
        self.set_lane(lane)
        self.set_width(width)
        self.set_depth(depth)
        self.set_always_on_top()

    def set_height(self, height):
        self.height = height
        invoke(Obstacle.set_fixed_height, self.body, height)
        invoke(Obstacle.set_y_position, self.body)

    def set_width(self, width):
        self.width = width
        invoke(Obstacle.set_fixed_width, self.body, width)

    def set_depth(self, depth):
        self.depth = depth
        invoke(Obstacle.set_fixed_depth, self.body, depth)
