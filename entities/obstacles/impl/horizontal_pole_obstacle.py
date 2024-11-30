from copy import copy

from ursina import Entity, color, invoke, Texture

from config.constants import LANE_WIDTH, CollisionType, ROAD_HEIGHT, CollisionSide
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.utils import left_outer_border_lane, left_inner_border_lane, right_inner_border_lane, right_outer_border_lane

class ObstaclePoleGate(LaneObstacle):
    def __init__(self, models,position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.dark_gray, height: float = 2.5,
                 width: float = LANE_WIDTH, depth: float = 1):
        super().__init__(models,position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)

        self.left_pole = Entity(
            model=copy(models.cube_standard),
            color=colorr,
            z=position_z,
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self,
            render_queue=3,
        )

        self.right_pole = Entity(
            model=copy(models.cube_standard),
            color=colorr,
            z=position_z,
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self,
            always_on_top=True
        )

        self.top_pole = Entity(
            model=copy(models.cube_standard),
            color=color.gray,
            texture=copy(models.pole_tex),
            z=position_z,
            collider='box',
            jump=True,
            climb=False,
            sign=False,
            parentt=self
        )

        self.children = [self.left_pole, self.right_pole, self.top_pole]

        self.set_height(height)
        self.set_depth(depth)
        self.set_lane(lane)
        self.set_width(width)
        self.set_always_on_top()

    def set_height(self, height):
        self.height = height

        invoke(Obstacle.set_fixed_height, self.left_pole, height)
        invoke(Obstacle.set_y_position, self.left_pole)
        invoke(Obstacle.set_fixed_height, self.right_pole, height)
        invoke(Obstacle.set_y_position, self.right_pole)

        self.top_pole.y = self.right_pole.y + (self.height + self.top_pole.bounds.size[2]) / 2

    def set_width(self, width):
        self.width = width
        offset = (width - (self.left_pole.x - self.right_pole.x) - 2) / 2
        self.right_pole.x = self.right_pole.x + offset
        self.left_pole.x = self.left_pole.x - offset
        invoke(Obstacle.set_fixed_width, self.top_pole, width)

    def set_depth(self, depth):
        self.depth = depth
        self.top_pole.y += (depth - self.top_pole.bounds.size[2]) / 2
        invoke(Obstacle.set_fixed_depth, self.right_pole, depth * 15)
        invoke(Obstacle.set_fixed_depth, self.left_pole, depth * 15)
        invoke(Obstacle.set_fixed_depth, self.top_pole, depth * 15)
        invoke(Obstacle.set_fixed_width, self.right_pole, depth)
        invoke(Obstacle.set_fixed_width, self.left_pole, depth)
        invoke(Obstacle.set_fixed_height, self.top_pole, depth)

    def check_collision_type(self, player_x, is_crouching, is_jumping, *args, **kwargs) -> CollisionType:
        """
        when the player is crouching the collision type is none if we are in the middle otherwise full or light
        depending on how close the player is to the ends
        """
        collision_type_full = (right_outer_border_lane(self.lane) <= player_x <= right_inner_border_lane(self.lane)) or (
                                left_outer_border_lane(self.lane) <= player_x <= left_inner_border_lane(self.lane))
        if collision_type_full:
            collision_type = CollisionType.FULL
        elif is_crouching and not is_jumping:
            collision_type_none = left_inner_border_lane(self.lane) < player_x < right_inner_border_lane(self.lane)
            if collision_type_none:
                collision_type = None
            else:
                collision_type = CollisionType.LIGHT
        else:
            collision_type = CollisionType.FULL

        return collision_type

    def check_collision_side(self, player_x, player_y, child, *args, **kwargs) -> CollisionSide:
        print(child.y, child.bounds.start[1], player_y)
        if player_y >= self.height + ROAD_HEIGHT / 2 - 1:
            collision_side = CollisionSide.UP
        else:
            if player_x < child.x:
                collision_side = CollisionSide.LEFT
            else:
                collision_side = CollisionSide.RIGHT

        return collision_side

    def set_colorr(self, colorr):
        self.right_pole.color = colorr
        self.left_pole.color = colorr
