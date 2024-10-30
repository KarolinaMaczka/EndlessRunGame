import os

from ursina import Entity, color, invoke, destroy

from config.config import config
from config.constants import ROAD_WIDTH, LANE_WIDTH
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle


class ObstaclePoleGate(LaneObstacle):
    def __init__(self, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.dark_gray, height: float = 2.5,
                 width: float = LANE_WIDTH, depth: float = 1):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)
        folder = config['horizontal_pole']['pole.folder']

        self.left_pole = Entity(
            model='cube',
            color=colorr,
            z=position_z,
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )

        self.right_pole = Entity(
            model='cube',
            color=colorr,
            z=position_z,
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )

        self.top_pole = Entity(
            model='cube',
            color=color.gray,
            texture=os.path.join(self.base_folder, folder, config['horizontal_pole']['pole.texture']),
            z=position_z,
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )
        self.children = [self.left_pole, self.right_pole, self.top_pole]

        self.set_depth(depth)
        self.set_lane(lane)
        self.set_height(height)
        self.set_width(width)

    # def delete(self):
        # destroy(self.top_pole)
        # destroy(self.right_pole)
        # destroy(self.left_pole)

    def set_height(self, height):
        self.height = height

        invoke(Obstacle.set_fixed_height, self.left_pole, height)
        invoke(Obstacle.set_y_position, self.left_pole)
        invoke(Obstacle.set_fixed_height, self.right_pole, height)
        invoke(Obstacle.set_y_position, self.right_pole)

        self.top_pole.y = self.right_pole.y + (height + self.top_pole.bounds.size[2]) / 2

    def set_width(self, width):
        self.width = width
        offset = (width - (self.left_pole.x - self.right_pole.x) - 2) / 2
        self.right_pole.x = self.right_pole.x + offset
        self.left_pole.x = self.left_pole.x - offset
        invoke(Obstacle.set_fixed_width, self.top_pole, width)

    # def set_lane(self, lane):
    #     self.lane = lane
    #     invoke(LaneObstacle.set_fixed_lane, self.right_pole, self.lane)
    #     invoke(LaneObstacle.set_fixed_lane, self.left_pole, self.lane)
    #     invoke(LaneObstacle.set_fixed_lane, self.top_pole, self.lane)

    def set_depth(self, depth):
        self.depth = depth
        self.top_pole.y += (depth - self.top_pole.bounds.size[2]) / 2
        invoke(Obstacle.set_fixed_depth, self.right_pole, depth * 5)
        invoke(Obstacle.set_fixed_depth, self.left_pole, depth * 5)
        invoke(Obstacle.set_fixed_depth, self.top_pole, depth * 5)
        invoke(Obstacle.set_fixed_width, self.right_pole, depth)
        invoke(Obstacle.set_fixed_width, self.left_pole, depth)
        invoke(Obstacle.set_fixed_height, self.top_pole, depth)

    # def set_z_position(self, position_z):
    #     self.position_z = position_z
    #     self.left_pole.z = position_z
    #     self.right_pole.z = position_z
    #     self.top_pole.z = position_z