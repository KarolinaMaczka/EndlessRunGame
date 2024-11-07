from ursina import Entity, color, invoke

from config.constants import LANE_WIDTH, STANDARD_OBSTACLE_HEIGHT, CollisionType, ROAD_WIDTH
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.utils import left_inner_border_lane, left_outer_border_lane, right_outer_border_lane, \
    right_inner_border_lane


class ObstacleBoard(ObstaclePoleGate):
    def __init__(self, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.dark_gray, height: float = 2.5,
                 width: float = LANE_WIDTH, depth: float = 1, board_height: float = STANDARD_OBSTACLE_HEIGHT):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)
        self.set_height(height, board_height)
        self.set_always_on_top()

    def set_height(self, height, board_height=STANDARD_OBSTACLE_HEIGHT):
        """
        :param height: height of poles under the board
        :param board_height: the total height of the board
        """
        self.height = board_height
        board_height -= height
        invoke(Obstacle.set_fixed_height, self.left_pole, height)
        invoke(Obstacle.set_y_position, self.left_pole)
        invoke(Obstacle.set_fixed_height, self.right_pole, height)
        invoke(Obstacle.set_y_position, self.right_pole)

        self.top_pole.y = self.right_pole.y + (height + board_height) / 2
        invoke(Obstacle.set_fixed_height, self.top_pole, board_height)

    def check_collision_type(self, player_x, is_crouching, *args, **kwargs) -> CollisionType:
        collision_type_full = (right_inner_border_lane(self.lane) <= player_x <= right_outer_border_lane(
            self.lane)) or (left_outer_border_lane(self.lane) <= player_x <= left_inner_border_lane(self.lane))
        if collision_type_full:
            collision_type = CollisionType.FULL
        elif is_crouching:
            collision_type_none = left_inner_border_lane(self.lane) < player_x < right_inner_border_lane(self.lane)
            if collision_type_none:
                collision_type = None
            else:
                collision_type = CollisionType.LIGHT
        else:
            collision_type = CollisionType.FULL

        return collision_type

