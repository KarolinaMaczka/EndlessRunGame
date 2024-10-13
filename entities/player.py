from ursina import FrameAnimation3d, time
from config.config import config
from config.constants import SLIGHT_BOUNCE_DIST, CollisionSide, CollisionType


class Player(FrameAnimation3d):

    def __init__(self):
        super().__init__(config['player']['player.object'],
                         texture=config['player']['player.texture'],
                         double_sided=True, position=(0, 2, 0), collider='box',
                         scale=5)
        self.speed = 200

        self.velocity_y = 0
        self.is_jumping = False
        self.gravity = -0.5
        self.jump_height = 1

    def set_jump(self):
        self.velocity_y = self.jump_height
        self.is_jumping = True

    def run(self):
        self.z += time.dt * self.speed

    def run_faster(self):
        self.z += time.dt * 400

    def go_left(self):
        self.x -= time.dt * 25

    def go_right(self):
        self.x += time.dt * 25

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
