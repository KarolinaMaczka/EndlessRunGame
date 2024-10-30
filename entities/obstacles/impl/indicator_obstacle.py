import os
import random

from ursina import color, Entity, destroy

from ursina import color, Entity, invoke

from config.config import config
from config.constants import STANDARD_OBSTACLE_HEIGHT
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.sign_obstacle import ObstacleSign


class ObstacleIndicator(ObstacleSign):
    def __init__(self, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.brown, height: float = STANDARD_OBSTACLE_HEIGHT-3,
                 width: float = 4, depth: float = 1):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)
        folder = config['indicator']['indicator.folder']

        self.body = Entity(
            model=os.path.join(self.base_folder, folder, config['indicator']['indicator.object']),
            rotation=(0, random.choice([45, 135, 225, 315]), 0),
            color=colorr,
            z=position_z,
            collider='box',
            double_sided=True,
            jump=True,
            climb=False,
            sign=True,
            parentt=self
        )
        self.children = [self.body]


        self.set_height(height)
        self.set_lane(lane)
        self.set_width(width)
        self.set_depth(depth)

    def set_height(self, height):
        self.height = height

        invoke(Obstacle.set_fixed_height, self.body, height)
        invoke(Obstacle.set_y_position, self.body)

    # def set_lane(self, lane):
    #     self.lane = lane
    #     invoke(ObstacleSign.set_fixed_lane, self.body, self.lane)

    def set_width(self, width):
        self.width = width
        invoke(Obstacle.set_fixed_width, self.body, width)

    def set_depth(self, depth):
        self.depth = depth
        invoke(Obstacle.set_fixed_depth, self.body, depth)

    # def set_z_position(self, position_z):
    #     self.position_z = position_z
    #     self.position_z = position_z
    #     self.body.z = position_z

    # def delete(self):
    #     destroy(self.body)

# class ObstacleIndicator(Entity):
#     def __init__(self, position_x: float, position_y: float, position_z: float, entity_metadata):
#         super().__init__(position=(position_x, position_y, position_z))
#
#         self.platform = Entity(
#             model="assets/indicator/indicater2.obj",
#             scale=0.5,
#             # texture="assets/sign2/Sign_Diffuse.png",
#             rotation=(0, 45, 0),
#             color=color.brown,
#             position=(position_x, 5, position_z),
#             # collider='box',
#             # double_sided=True
#         )