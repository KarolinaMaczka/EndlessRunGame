import os
from copy import deepcopy, copy

from ursina import Entity, color, destroy, Texture, Cube, mesh_importer

from config.config import config
from config.constants import ROAD_WIDTH, ROAD_HEIGHT, LANE_WIDTH, CollisionType, CollisionSide, LANE_COUNT
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.utils import right_outer_border_lane, left_outer_border_lane


class ObstacleGate(Obstacle):
    def __init__(self, models,position_z: float, difficulty: int = 1, lane=None, height: float = 10, depth: float = 100, width: float = ROAD_WIDTH, colorr=color.brown):
        top_beam_height = 4
        super().__init__(models,position_z=position_z, difficulty=difficulty, lane=lane, height=height + top_beam_height,width=width, depth=depth)

        gap_between_pillars = ROAD_WIDTH // LANE_COUNT
        pillar_width = (width - gap_between_pillars) // 2
        position_x = 0
        position_y = ROAD_HEIGHT / 2

        self.left_pillar = Entity(
            model=copy(models.cube_standard),
            scale=(pillar_width, height, depth),
            color=colorr,
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
            model=copy(models.cube_standard),
            scale=(pillar_width, height, depth),
            color=colorr,
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
            model=copy(models.cube_standard),
            scale=(width, top_beam_height, depth),
            color=color.gray,
            position=(position_x, position_y + height + 1, position_z),
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )
        self.top_beam.texture_setter(copy(models.gate_tex))

        self.children = [self.top_beam, self.left_pillar, self.right_pillar]

        self.set_width(width)
        self.set_height(height + top_beam_height)
        self.set_depth(depth)
        self.set_lane()
        self.set_always_on_top()

    def set_lane(self, *args):
        self.lane = None

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_depth(self, depth):
        self.depth = depth

    def check_collision_type(self, player_x, child, *args, **kwargs) -> CollisionType:
        if child is self.top_beam:
            return CollisionType.FULL
        collision_type = left_outer_border_lane(LANE_COUNT//2) < player_x < right_outer_border_lane(LANE_COUNT//2)
        collision_type = CollisionType.LIGHT if collision_type else CollisionType.FULL
        return collision_type

    def set_colorr(self, colorr):
        self.right_pillar.color = colorr
        self.left_pillar.color = colorr
