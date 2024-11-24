from ursina import time, Entity

from config.constants import CollisionSide, CollisionType


class Player(Entity):

    def __init__(self):
        super().__init__(
            # model="assets/player/Wolf_obj",
            # texture="assets/player/textures/Wolf_Body",
            # model='cube',
            name='player',
            # render_queue=0,
             double_sided=True, position=(0, 2, 0), collider='box',
             scale=5, rotation=(0,0,0), fps=5,
            visible=False
        ),

        self.set_values()

    def set_jump(self):
        self.velocity_y += self.jump_height
        self.is_jumping = True

    def set_climb(self, climb_height):
        self.is_climbing = True
        self.prev_speed = self.speed if self.speed else self.prev_speed
        self.speed = 0
        self.climb_height = climb_height

    def stop_climb(self):
        self.y = self.climb_height + 1
        self.velocity_y = 0
        self.speed = self.prev_speed
        self.is_climbing = False
        self.is_falling = True
        self.ground = self.climb_height + 1

    def land(self, ground_y):
        self.y = ground_y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_falling = False

    def crouch(self):
        self.is_crouching = True

    def reset(self):
        # self.context.player.scale = 5
        self.is_crouching = False

    def set_values(self):
        self.z = 0
        self.x = 0
        self.speed = 250
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_height = 0.55
        self.is_climbing = False
        self.climb_height = 0
        self.is_falling = False
        self.ground = 1
        self.climb_speed = 20
        self.velocity_x = 30
        self.prev_speed = self.speed
        self.is_crouching = False
        self.bouncing_dist = 3
        self.gravity = -1

    def fall_down(self):
        gravity = self.gravity
        if self.is_crouching:
            gravity *= 2

        self.velocity_y += gravity * time.dt
        self.y += self.velocity_y

    def run(self):
        self.z += time.dt * self.speed

    def run_faster(self):
        self.z += time.dt * 200

    def go_left(self):
        self.x -= time.dt * self.velocity_x

    def go_right(self):
        self.x += time.dt * self.velocity_x

    def bounce(self, side: CollisionSide = CollisionSide.LEFT,
               collision_type: CollisionType = CollisionType.LIGHT):
        self.visible = False if collision_type == CollisionType.FULL else True

        if side == CollisionSide.LEFT:
            self.x -= self.bouncing_dist
        elif side == CollisionSide.RIGHT:
            self.x += self.bouncing_dist
        elif side == CollisionSide.UP:
            self.z += self.bouncing_dist
        elif side == CollisionSide.DOWN:
            self.z -= self.bouncing_dist
