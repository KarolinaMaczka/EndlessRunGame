import random

from ursina import time, held_keys

from entities.camera import PlayerCamera
from config.constants import BOUNCE_DIST, COLLISION_DIST, SLIGHT_COLLISION_DIST, CollisionType, CollisionSide, \
    LANE_WIDTH, ROAD_HEIGHT
from entities.obstacles.impl.gate_obstacle import ObstacleGate
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.obstacle import Obstacle
from entities.player import Player
from typing import Optional, Tuple
from entities.obstacles.impl.board_obstacle import ObstacleBoard


class PhysicsEngine:
    def __init__(self, player: Player, camera: PlayerCamera):
        self.player = player
        self.camera = camera
        self.gravity = -1.5
        self.stop_jump = False
        self.prev_speed = 0

    def apply_gravity(self, obstacles):
        '''
        If player is climbing we move up till a certain point
        The default is to fall down up to a ground level
        :param obstacles: list of active obstacles
        '''

        if self.player.is_climbing:
            self.player.y += self.player.climb_speed * time.dt

            if self.player.y >= self.player.climb_height:
                # stop climb
                self.player.y = self.player.climb_height + 1
                self.player.velocity_y = 0
                self.player.speed = self.prev_speed
                self.player.is_climbing = False
                self.player.is_falling = True
                self.player.ground = self.player.climb_height + 1
        else:
            self.player.velocity_y += self.gravity * time.dt
            self.player.y += self.player.velocity_y

            ground_y = self.get_ground_height(obstacles)

            if held_keys['s']:
                self.player.velocity_y = self.gravity * 2

            if self.player.y <= ground_y:
                # landing
                self.player.y = ground_y
                self.player.velocity_y = 0
                self.player.is_jumping = False
                self.player.is_falling = False
            else:
                self.player.is_falling = True

    def get_ground_height(self, obstacles):
        ground_y = 1
        for obstacle in obstacles:
            is_colliding_z = obstacle.position_z - obstacle.depth <= self.player.z <= obstacle.position_z + obstacle.depth
            if obstacle.lane is not None:
                is_colliding_x = -25 + 10 * obstacle.lane <= self.player.x <= -15 + 10 * obstacle.lane
            else:
                is_colliding_x = True
            if is_colliding_x and is_colliding_z:
                obstacle_top_y = obstacle.height + 2
                if obstacle_top_y > ground_y and self.player.y >= obstacle_top_y:
                    ground_y = obstacle_top_y + 1
        return ground_y + 1

    def handle_player_collisions(self):
        stop = self.handle_road_collision() or self.handle_obstacle_collision()
        return stop

    def handle_road_collision(self):
        collision_type, side = self.check_road_collision()
        if collision_type:
            self.__handle_light_collision(side, collision_type)
        return False

    def handle_obstacle_collision(self):
        if hit_info := self.player.intersects():
            obstacle = hit_info.entity

            if obstacle.climb or self.player.is_climbing:
                self.player.is_climbing = True
                self.prev_speed = self.player.speed if self.player.speed else self.prev_speed
                self.player.speed = 0
                self.player.climb_height = obstacle.bounds.end.y + 2
                pass
            else:
                collision_type, side = self.check_collision(hit_info)

                if side == CollisionSide.UP and not obstacle.jump:
                    print(f"UP COLLISION zderzenie z przeszkodą na pozycji: {obstacle.position}, {self.player.position}")
                    self.__handle_full_collision(side, collision_type)
                    return True
                elif obstacle.sign or collision_type == CollisionType.LIGHT:
                    print(f"Lekkie zderzenie z przeszkodą na pozycji: {obstacle.position}, {self.player.position}")
                    self.__handle_light_collision(side, collision_type)
                elif collision_type == CollisionType.FULL:
                    print(f'parent {obstacle.parentt}, child {obstacle.parentt.children}, {obstacle}')
                    print(f"Mocne zderzenie z przeszkodą na pozycji: {obstacle.position}, {self.player.position}")
                    self.__handle_full_collision(side, collision_type)
                    return True

        return False

    def __handle_light_collision(self, side, collision_type):
        self.camera.shake_camera(duration=0.01, magnitude=0.05)
        self.player.bounce(side=side, collision_type=collision_type)

    def __handle_full_collision(self, side, collision_type):
        self.camera.shake_camera(duration=0.1, magnitude=0.3)
        self.player.bounce(side=side, collision_type=collision_type)

    def check_road_collision(self) -> Tuple[Optional[CollisionType], Optional[CollisionSide]]:
        if self.player.x >= 25:
            self.player.x = 25
            return CollisionType.LIGHT, CollisionSide.LEFT
        if self.player.x <= -25:
            self.player.x = -25
            return CollisionType.LIGHT, CollisionSide.RIGHT
        return None, None

    def check_collision(self, hit_info) -> Tuple[Optional[CollisionType], Optional[CollisionSide]]:
        obstacle = hit_info.entity


        # Check for collision type
        if obstacle.parentt.lane is not None:
            collision_type = -25 + 10 * obstacle.parentt.lane + 0.5 <= self.player.x <= -15 + 10 * obstacle.parentt.lane - 0.5
        elif type(obstacle.parentt) == ObstacleGate:
            collision_type = CollisionType.FULL if abs(
                self.player.x - obstacle.x) < LANE_WIDTH - 2 else CollisionType.LIGHT

        collision_type = CollisionType.FULL if collision_type else CollisionType.LIGHT

        if type(obstacle.parentt) == ObstacleBoard:
            if held_keys['s']:
                collision_type = CollisionType.FULL if abs(
                    self.player.x - obstacle.x) < LANE_WIDTH / 4 - 1 else CollisionType.LIGHT
            else:
                collision_type = CollisionType.FULL

        if self.player.y >= obstacle.parentt.height + ROAD_HEIGHT / 2 - 1:
            collision_side = CollisionSide.UP
        elif obstacle.bounds.start.y >= self.player.y:
            collision_side = CollisionSide.DOWN
            collision_type = CollisionType.FULL # sides are relative to object not player
        else:
            if self.player.x < obstacle.x:
                collision_side = CollisionSide.LEFT
            else:
                collision_side = CollisionSide.RIGHT

        return collision_type, collision_side

