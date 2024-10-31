import random

from ursina import time

from entities.camera import PlayerCamera
from config.constants import CollisionType, CollisionSide

from entities.obstacles.utils import right_border_lane, left_border_lane
from entities.player import Player
from typing import Optional, Tuple


class PhysicsEngine:
    def __init__(self, player: Player, camera: PlayerCamera):
        self.player = player
        self.camera = camera
        self.gravity = -1
        self.stop_jump = False
        # self.prev_speed = 0

    def apply_gravity(self, obstacles):
        '''
        If player is climbing we move up till a certain point
        The default is to fall down up to a ground level
        :param obstacles: list of active obstacles
        '''

        if self.player.is_climbing:
            self.player.y += self.player.climb_speed * time.dt
            if self.player.y >= self.player.climb_height:
                self.player.stop_climb()
        else:
            ground_y = self.get_ground_height(obstacles)
            self.player.fall_down(self.gravity)

            if self.player.y <= ground_y:
                self.player.land(ground_y)

    def get_ground_height(self, obstacles):
        ground_y = 1

        for obstacle in obstacles:
            # for child in obstacle.children:
            #     if not child.jump:
            #         return ground_y
            is_colliding_z = obstacle.position_z - obstacle.depth <= self.player.z <= obstacle.position_z + obstacle.depth

            if obstacle.lane is not None:
                is_colliding_x = left_border_lane(obstacle.lane) <= self.player.x <= right_border_lane(obstacle.lane)
            else:
                is_colliding_x = True

            if is_colliding_x and is_colliding_z:
                obstacle_top_y = obstacle.height + 2
                if ground_y < obstacle_top_y <= self.player.y:
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
        print(self.player.y)
        if hit_info := self.player.intersects():
            obstacle = hit_info.entity

            if obstacle.climb:
                self.player.set_climb(climb_height=obstacle.bounds.end.y + 3)
                return False
            elif self.player.is_climbing:
                return False
            else:
                collision_type, side = self.check_collision(obstacle)

                if side == CollisionSide.UP:
                    if not obstacle.jump:
                        print(f"UP collision with obstacle:  {obstacle.position}, {self.player.position}")
                        self.__handle_full_collision(side, collision_type)
                        return True
                    return False
                elif side == CollisionSide.DOWN:
                    print(f"DOWN collision with obstacle {type(obstacle.parentt).__name__}:  {obstacle.position}, {self.player.position}")
                    return False
                elif obstacle.sign or collision_type == CollisionType.LIGHT:
                    print(f"LIGHT {side} collision with obstacle {type(obstacle.parentt).__name__}: {obstacle.position}, {self.player.position}")
                    self.__handle_light_collision(side, collision_type)
                    return False
                elif collision_type == CollisionType.FULL:
                    print(f"FULL {side} collision with obstacle {type(obstacle.parentt).__name__}: {obstacle.position}, {self.player.position}")
                    self.__handle_full_collision(side, collision_type)
                    return True
        return False

    def check_road_collision(self) -> Tuple[Optional[CollisionType], Optional[CollisionSide]]:
        if self.player.x >= 25:
            self.player.x = 25
            return CollisionType.LIGHT, CollisionSide.LEFT
        if self.player.x <= -25:
            self.player.x = -25
            return CollisionType.LIGHT, CollisionSide.RIGHT
        return None, None

    def check_collision(self, obstacle) -> Tuple[Optional[CollisionType], Optional[CollisionSide]]:
        collision_type = obstacle.parentt.check_collision_type(player_x=self.player.x, player_y=self.player.y,
                                                               player_z=self.player.z, child=obstacle,
                                                               is_crouching=self.player.is_crouching,
                                                               is_jumping=self.player.is_jumping)
        collision_side = obstacle.parentt.check_collision_side(player_x=self.player.x, player_y=self.player.y,
                                                               player_z=self.player.z, child=obstacle)

        return collision_type, collision_side

    def __handle_light_collision(self, side, collision_type):
        self.camera.shake_camera(duration=0.01, magnitude=0.05)
        self.player.bounce(side=side, collision_type=collision_type)

    def __handle_full_collision(self, side, collision_type):
        self.camera.shake_camera(duration=0.1, magnitude=0.3)
        self.player.bounce(side=side, collision_type=collision_type)
