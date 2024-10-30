import os

from ursina import Entity, color, destroy

from config.config import config
from config.constants import ROAD_WIDTH, ROAD_HEIGHT
from entities.obstacles.obstacle import Obstacle


class ObstacleGate(Obstacle):
    def __init__(self, position_z: float, difficulty: int = 1, lane=None, height: float = 10, depth: float = 100, width: float = ROAD_WIDTH):
        top_beam_height = 4
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height + top_beam_height,width=width, depth=depth)

        gap_between_pillars = ROAD_WIDTH // 5
        pillar_width = (width - gap_between_pillars) // 2
        position_x = 0
        position_y = ROAD_HEIGHT / 2
        folder = config['gate']['gate.folder']

        self.left_pillar = Entity(
            model='cube',
            scale=(pillar_width, height, depth),
            color=color.brown,
            texture='brick',
            position=(position_x - gap_between_pillars / 2 - pillar_width / 2,
                      position_y + height / 2, position_z),
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )

        self.right_pillar = Entity(
            model='cube',
            scale=(pillar_width, height, depth),
            color=color.brown,
            texture='brick',
            position=(position_x + gap_between_pillars / 2 + pillar_width / 2,
                      position_y + height / 2, position_z),
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )

        self.top_beam = Entity(
            model='cube',
            scale=(width, top_beam_height, depth),
            color=color.gray,
            texture=os.path.join(self.base_folder, folder, config['gate']['top_beam.texture']),
            position=(position_x, position_y + height + 1, position_z),
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )
        self.children = [self.top_beam, self.left_pillar, self.right_pillar]

        self.set_width(width)
        self.set_height(height + top_beam_height)
        self.set_depth(depth)


    # def delete(self):
    #     destroy(self.top_beam)
    #     destroy(self.right_pillar)
    #     destroy(self.left_pillar)

    # def set_z_position(self, position_z):
    #     self.position_z = position_z
    #     self.top_beam.z = position_z
    #     self.right_pillar.z = position_z
    #     self.left_pillar.z = position_z

    def set_lane(self, *args):
        pass

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_depth(self, depth):
        self.depth = depth

