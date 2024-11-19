# import random
# from dataclasses import dataclass, field
# from typing import List
#
# from config.constants import LANE_COUNT, Color
# from difficulty.maps.map import ObstacleMap
# from entities.obstacles.impl.board_obstacle import ObstacleBoard
# from entities.obstacles.impl.cube_obstacle import ObstacleCube
# from entities.obstacles.impl.fence_obstacle import ObstacleFence
# from entities.obstacles.impl.gate_obstacle import ObstacleGate
# from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
# from entities.obstacles.impl.long_cube import ObstacleLongCube
# from entities.obstacles.impl.train_obstacle import ObstacleTrain
# from entities.obstacles.impl.wooden_sign_obstacle import ObstacleWoodenSign
# from entities.obstacles.impl.indicator_obstacle import ObstacleIndicator
# from entities.obstacles.obstacle_metadata_factory import ObstacleFactory
#
#
# @dataclass
# class SeventhObstacleMap(ObstacleMap):
#     """
#     signs: yes
#     trains: yes,
#     small obstacles: yes
#     gates: yes
#     small obstacles and trains are always at the same z position
#     Train are next to each other
#     Use only when generation distance is at least 300
#     small obstacles cannot be next to each other
#     """
#     def generate_obstacles(self, obstacle_generation_distance, start, length):
#         last_obstacle_z = start + obstacle_generation_distance
#         end = start + length
#         start_x = random.randint(0, 1)
#
#         self.obstacles = []
#         while last_obstacle_z <= end+100:
#             if random.random() < self.lane_change_const:
#                 if obstacle_generation_distance <= 150:
#                     last_obstacle_z += obstacle_generation_distance
#
#                 start_x = int(not start_x)
#
#             self._create_signs(z_position=last_obstacle_z - obstacle_generation_distance / 2)
#             if random.random() < self.gate_generation_const:
#                 if obstacle_generation_distance <= 150:
#                     last_obstacle_z += obstacle_generation_distance
#                 self._generate_gate(last_obstacle_z)
#                 if obstacle_generation_distance <= 150:
#                     last_obstacle_z += obstacle_generation_distance
#             else:
#                 self._create_trains(start_x, last_obstacle_z)
#                 self._create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
#             last_obstacle_z += obstacle_generation_distance
#         return last_obstacle_z
#
#     def _create_trains(self, start_x: int, z_position: float):
#         for lane in range(start_x, LANE_COUNT, 2):
#             self.obstacles.append(self._big_obstacles.create_obstacle(z_position, lane))
#
#     def _create_small_obstacles(self, start_x: int, z_position: float, small_obstacle_const):
#         for lane in range(start_x, LANE_COUNT, 2):
#             if random.random() < small_obstacle_const:
#                 self.obstacles.append(self._small_obstacles.create_obstacle(z_position, lane))