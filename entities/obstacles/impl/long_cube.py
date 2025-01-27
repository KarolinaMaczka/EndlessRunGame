import random
from copy import copy

from ursina import Entity, color, invoke

from config.config import config
from config.constants import LANE_WIDTH, CollisionType
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle


class ObstacleLongCube(LaneObstacle):
    def __init__(self, models,position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.orange,
                 has_ladder: float = 0.9, height: float = 10,
                 width: float = LANE_WIDTH - 1, depth: float = 100):
        super().__init__(models,position_z=position_z, difficulty=difficulty, lane=lane, height=height, width=width,
                         depth=depth)

        self.body = Entity(
            model=copy(models.cube_standard),
            scale=(width, height, depth),
            color=colorr,
            z=position_z,
            collider='box',
            double_sided=True,
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )
        self.body.texture_setter(copy(models.container_tex))

        self.children = [self.body]
        self.ladder = None
        if random.random() < has_ladder:
            self.ladder = Entity(
                model=copy(models.container),
                scale=(8, 1.3, 40),
                rotation=(0, 0, 0),
                color=color.blue,
                z=position_z - depth / 2 + 1,
                collider='box',
                double_sided=True,
                jump=True,
                climb=True,
                sign=False,
                parentt=self
            )
            self.children = [self.body, self.ladder]

        self.set_depth(depth)
        self.set_lane(lane)
        self.set_height(height)
        self.set_width(width)
        self.set_always_on_top()

    def set_width(self, width):
        self.width = width
        invoke(Obstacle.set_fixed_width, self.body, width)
        if self.ladder:
            invoke(Obstacle.set_fixed_width, self.ladder, (width + 2) / 2)

    def set_height(self, height):
        self.height = height

        invoke(Obstacle.set_fixed_height, self.body, height)
        invoke(Obstacle.set_y_position, self.body)
        if self.ladder:
            invoke(Obstacle.set_fixed_height, self.ladder, height + 0.5)
            invoke(Obstacle.set_y_position, self.ladder)

    def set_depth(self, depth):
        self.depth = depth
        invoke(Obstacle.set_fixed_depth, self.body, depth)

    def set_colorr(self, colorr):
        self.body.color = colorr

    def set_has_ladder(self, has_ladder):
        if random.random() < has_ladder:
            mod = copy(self.models.cube_standard)
            self.ladder = Entity(
                model=mod,
                scale=(8, 1.3, 10),
                rotation=(0, 0, 0),
                color=color.blue,
                z=self.position_z - self.depth / 2 - 1,
                collider='box',
                double_sided=True,
                jump=True,
                climb=True,
                sign=False,
                parentt=self
            )
            self.children = [self.body, self.ladder]
        else:
            self.ladder = None
            self.children = [self.body]

    def set_position_z(self, position_z):
        self.z = position_z
        self.position_z = position_z
        self.body.position_z = position_z
        if self.ladder is not None:
            self.ladder.position_z = self.position_z - self.depth / 2 - 2.5

    def check_collision_type(self, player_x, player_y, player_z, child, *args, **kwargs) -> CollisionType | None:
        if len(self.children) > 1 and player_z < self.position_z - 4 and abs(player_x - child.x) < LANE_WIDTH / 2 - 1:
            return None

        collision_type = CollisionType.FULL if abs(player_x - child.x) < LANE_WIDTH / 2 - 1 else CollisionType.LIGHT
        return collision_type
