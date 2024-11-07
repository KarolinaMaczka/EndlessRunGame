import os

from ursina import Entity, color, invoke, destroy

from config.config import config
from config.constants import LANE_WIDTH
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle


class ObstacleTrain(LaneObstacle):
    def __init__(self, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.orange, height: float = 10,
                 width: float = LANE_WIDTH - 1, depth: float = 100):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)
        folder = config['train']['train.folder']

        self.body = Entity(
            model=os.path.join(self.base_folder, folder, config['train']['train.object']),
            texture=os.path.join(self.base_folder, folder, config['train']['train.texture']),
            color=colorr,
            z=position_z,
            collider='box',
            double_sided=True,
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )
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
