import os

from ursina import color, Entity, invoke

from config.config import config
from config.constants import LANE_WIDTH, CollisionType, CollisionSide, ROAD_WIDTH, ROAD_HEIGHT
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.utils import left_inner_border_lane, right_inner_border_lane


class ObstacleFence(LaneObstacle):
    def __init__(self, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.brown, height: float = 4.5,
                 width: float = LANE_WIDTH - 2, depth: float = 4):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height, width=width,
                         depth=depth)

        folder = config['fence']['fence.folder']
        self.body = Entity(
            model=os.path.join(self.base_folder, folder, config['fence']['fence.object']),
            scale=(0.4, 0.05, 0.05),
            texture=os.path.join(self.base_folder, folder, config['fence']['fence.texture']),
            rotation=(0, 90, 0),
            color=colorr,
            z=position_z,
            collider='box',
            double_sided=True,
            jump=False,
            climb=False,
            sign=False,
            parentt=self
        )
        self.children = [self.body]

        self.set_depth(depth)
        self.set_height(height)
        self.set_width(width)
        self.set_lane(lane)
        self.set_always_on_top()

    def set_width(self, width):
        self.width = width
        invoke(Obstacle.set_fixed_depth, self.body, width)

    def set_height(self, height):
        self.height = height
        invoke(Obstacle.set_fixed_height, self.body, height)
        invoke(Obstacle.set_y_position, self.body)

    def set_lane(self, lane):
        self.lane = lane
        invoke(LaneObstacle.set_fixed_lane, self.body, self.lane)
        self.body.x += -ROAD_WIDTH // 2 + self.lane * LANE_WIDTH + (LANE_WIDTH - self.width) // 2 - self.body.x - self.body.bounds.start[2]

    def set_depth(self, depth):
        self.depth = depth
        invoke(Obstacle.set_fixed_width, self.body, depth)

    def check_collision_type(self, player_x, player_y, player_z, child, *args, **kwargs) -> CollisionType:
        # collision_type = CollisionType.FULL if abs(player_x - child.x) < LANE_WIDTH / 2 - 1 else CollisionType.LIGHT
        collision_type = left_inner_border_lane(self.lane) < player_x < right_inner_border_lane(self.lane)
        collision_type = CollisionType.FULL if collision_type else CollisionType.LIGHT

        return collision_type

    def check_collision_side(self, player_x, player_y, child, *args, **kwargs) -> CollisionSide:
        if player_y >= self.height + ROAD_HEIGHT / 2 - 1:
            collision_side = CollisionSide.UP
        elif child.bounds.start.y >= player_y:
            collision_side = CollisionSide.DOWN
        else:
            collision_side = CollisionSide.RIGHT if -ROAD_WIDTH / 2 + LANE_WIDTH * (
                self.lane) <= player_x else CollisionSide.LEFT

        return collision_side
