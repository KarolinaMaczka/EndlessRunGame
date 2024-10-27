from ursina import FrameAnimation3d, time, color
from config.config import config
from config.constants import SLIGHT_BOUNCE_DIST, CollisionSide, CollisionType


class Player(FrameAnimation3d):

    def __init__(self):
        super().__init__(
            # config['player']['player.object'],
            #  texture=config['player']['player.texture'],
            name='player',
             double_sided=True, position=(0, 1, 0), collider='box',
             scale=5, rotation=(0,10,0), fps=5)
        self.speed = 250

        self.velocity_y = 0
        self.is_jumping = False
        self.jump_height = 0.5
        self.is_climbing = False
        self.climb_height = 0
        self.is_falling = False
        self.ground = 1
        self.climb_speed = 10
        self.velocity_x = 30

    def set_jump(self):
        self.velocity_y += self.jump_height
        self.is_jumping = True

    def set_climb(self, climb_height):
        self.velocity_y = climb_height
        self.is_climbing = True

    def run(self):
        self.z += time.dt * self.speed

    def run_faster(self):
        self.z += time.dt * 200

    def go_left(self):
        self.x -= time.dt * self.velocity_x

    def go_right(self):
        self.x += time.dt * self.velocity_x

    def bounce(self, dist=SLIGHT_BOUNCE_DIST, side: CollisionSide = CollisionSide.LEFT,
               collision_type: CollisionType = CollisionType.LIGHT):
        self.visible = False if collision_type == CollisionType.FULL else True

        if side == CollisionSide.LEFT:
            self.x -= dist
        elif side == CollisionSide.RIGHT:
            self.x += dist
        elif side == CollisionSide.UP:
            self.z += dist
        elif side == CollisionSide.DOWN:
            self.z -= dist
