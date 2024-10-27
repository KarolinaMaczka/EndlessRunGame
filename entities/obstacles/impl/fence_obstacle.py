import os

from ursina import color, Entity, invoke, destroy

from config.config import config
from config.constants import LANE_WIDTH, CollisionType, CollisionSide
from entities.obstacles.lane_obstacle import LaneObstacle
from entities.obstacles.obstacle import Obstacle


class ObstacleFence(LaneObstacle):
    def __init__(self, position_z: float, difficulty: int = 1, lane: int = 0, colorr=color.brown, height: float = 4.5, width: float = LANE_WIDTH - 2, depth: float = 4):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height,width=width, depth=depth)

        folder = config['fence']['fence.folder']
        self.body = Entity(
            model=os.path.join(self.base_folder, folder, config['fence']['fence.object']),
            scale=(0.4, 0.05, 0.05),
            texture=os.path.join(self.base_folder, folder, config['fence']['fence.texture']),
            rotation=(0, 90, 0),
            color=color.brown,
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
        self.set_lane(lane)
        self.set_height(height)
        self.set_width(width)


    # def delete(self):
    #     destroy(self.body)

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
        self.body.x += self.body.bounds.size[0] * 0.9

    def set_depth(self, depth):
        self.depth = depth
        invoke(Obstacle.set_fixed_width, self.body, depth)

    # def set_z_position(self, position_z):
    #     self.position_z = position_z
    #     self.body.z = position_z

    def check_collision(self, player):
        lanes = {0: (-25, -15), 1: (-15, -5), 2: (-5,5), 3: (5,15), 4: (15,25)}
        if self.body.intersects():
            if player.y > self.body.bounds.end.y:
                return None, None
                collision_side = CollisionSide.UP
            elif lanes[self.lane][0] <= player.x and lanes[self.lane][1] >= player.x:
                middle = (lanes[self.lane][0] + lanes[self.lane][1]) / 2
                if player.x < middle:
                    collision_side = CollisionSide.LEFT
                elif player.x > middle:
                    collision_side = CollisionSide.RIGHT
            # elif player.y < self.body.bounds.start.y:
            #     collision_side = CollisionSide.DOWN
            # elif player.y > self.body.bounds.end.y:
            #     collision_side = CollisionSide.UP
            else:
                collision_side = CollisionSide.UP if player.z < self.body.bounds.start.z else CollisionSide.DOWN

            # Determine collision type based on relative speed or proximity (simplified here)
            collision_type = CollisionType.FULL if abs(player.x - self.body.x) < LANE_WIDTH / 2 - 1 else CollisionType.LIGHT
            print(f"collision side {collision_side}")
            return collision_type, collision_side

        return None, None