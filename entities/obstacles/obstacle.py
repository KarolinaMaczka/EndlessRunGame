from abc import abstractmethod
from dataclasses import dataclass
from typing import Tuple

from typing_extensions import Optional
from ursina import Entity, destroy

from config.constants import CollisionType, CollisionSide, LANE_WIDTH, ROAD_HEIGHT


class Obstacle(Entity):
    def __init__(self, position_z: float, difficulty: int, lane: int, height: float, width: float, depth: float):
        super().__init__(z=position_z)
        self.children = []
        self.difficulty = difficulty
        self.lane = lane
        self.base_folder = 'assets'
        self.position_z = position_z
        self.height = height
        self.width = width
        self.depth = depth

    @staticmethod
    def set_fixed_width(obj, fixed_width):
        original_width = obj.bounds.size[0]
        new_scale = fixed_width / original_width
        obj.scale_x *= new_scale

    @staticmethod
    def set_fixed_depth(obj, fixed_depth):
        original_depth = obj.bounds.size[2]
        new_scale = fixed_depth / original_depth
        obj.scale_z *= new_scale

    @staticmethod
    def set_fixed_height(obj, fixed_height):
        original_height = obj.bounds.size[1]
        new_scale = fixed_height / original_height
        obj.scale_y *= new_scale

    @staticmethod
    def set_y_position(obj):
        current_bottom_y = obj.y + obj.bounds.start[1]
        offset = 1 - current_bottom_y
        obj.y += offset

    @abstractmethod
    def set_lane(self, lane):
        self.lane = lane

    def delete(self):
        for child in self.children:
            destroy(child)
        destroy(self)

    def set_position_z(self, position_z):
        self.position_z = position_z
        for child in self.children:
            child.z = position_z

    def set_colorr(self, colorr):
        for child in self.children:
            child.color = colorr

    def check_collision_type(self, player_x, player_y, player_z, child, *args, **kwargs) -> CollisionType:
        collision_type = CollisionType.FULL if abs(player_x - child.x) < LANE_WIDTH / 2 - 1 else CollisionType.LIGHT
        return collision_type

    def check_collision_side(self, player_x, player_y, child, *args, **kwargs) -> CollisionSide:
        if player_y >= self.height + ROAD_HEIGHT / 2 - 1:
            collision_side = CollisionSide.UP
        elif child.bounds.start.y >= player_y:
            collision_side = CollisionSide.DOWN
        else:
            if player_x < child.x:
                collision_side = CollisionSide.LEFT
            else:
                collision_side = CollisionSide.RIGHT

        return collision_side

    def set_always_on_top(self):
        for child in self.children:
            child.always_on_top = 0
