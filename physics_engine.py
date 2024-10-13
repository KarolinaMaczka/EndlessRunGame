from ursina import time

from entities.camera import PlayerCamera
from config.constants import BOUNCE_DIST, COLLISION_DIST, SLIGHT_COLLISION_DIST, CollisionType, CollisionSide
from entities.obstacles.obstacle import Obstacle
from entities.player import Player
from typing import Optional, Tuple


class PhysicsEngine:
    def __init__(self, player: Player, camera: PlayerCamera):
        self.player = player
        self.camera = camera
        self.gravity = -0.5

    def apply_gravity(self):
        self.player.velocity_y += self.gravity * time.dt
        self.player.y += self.player.velocity_y

        if self.player.y <= 1:
            self.player.y = 1
            self.player.velocity_y = 0
            self.player.is_jumping = False

    def handle_player_collisions(self, obstacles: list[Obstacle]):
        stop = self.handle_road_collision() or self.handle_obstacle_collision(obstacles)
        return stop

    def handle_road_collision(self):
        collision_type, side = self.check_road_collision()
        if collision_type:
            self.player.bounce(dist=BOUNCE_DIST, side=side, collision_type=collision_type)
            self.camera.shake_camera(duration=0.2, magnitude=0.1)

        return False

    def handle_obstacle_collision(self, obstacles: list[Obstacle]):
        # TODO if we go too fast it does not detect collisions properly
        for obstacle in obstacles:
            collision_type, side = self.check_collision(obstacle)
            if collision_type == CollisionType.FULL:
                print(f"Mocne zderzenie z przeszkodą na pozycji: {obstacle.position}, {self.player.position}")
                self.camera.shake_camera(duration=0.1, magnitude=0.3)
                self.player.bounce(side=side, collision_type=collision_type)
                return True
            elif collision_type == CollisionType.LIGHT:
                print(f"Lekkie zderzenie z przeszkodą na pozycji: {obstacle.position}, {self.player.position}")
                self.camera.shake_camera(duration=0.2, magnitude=0.1)
                self.player.bounce(side=side, collision_type=collision_type)
        return False

    def check_road_collision(self) -> Tuple[Optional[CollisionType], Optional[CollisionSide]]:
        if self.player.x >= 22:
            self.player.x = 22
            return CollisionType.LIGHT, CollisionSide.LEFT
        if self.player.x <= -22:
            self.player.x = -22
            return CollisionType.LIGHT, CollisionSide.RIGHT

        return None, None

    def check_collision(self, obstacle: Obstacle) -> Tuple[Optional[CollisionType], Optional[CollisionSide]]:
        x_distance = abs(self.player.x - obstacle.x)
        z_distance = abs(self.player.z - obstacle.z)
        distance = max(x_distance, z_distance)

        # Check for collision type
        if distance < COLLISION_DIST:
            collision_type = CollisionType.FULL
        elif distance < SLIGHT_COLLISION_DIST:
            collision_type = CollisionType.LIGHT
        else:
            return None, None

        # Determine the side of the collision
        if x_distance > z_distance:
            if self.player.x < obstacle.x:
                collision_side = CollisionSide.LEFT
            else:
                collision_side = CollisionSide.RIGHT
        else:
            if self.player.z < obstacle.z:
                collision_side = CollisionSide.UP
            else:
                collision_side = CollisionSide.DOWN

        return collision_type, collision_side
