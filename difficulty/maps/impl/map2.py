import random
from dataclasses import dataclass, field
from typing import List

from ursina import color

from config.constants import LANE_COUNT
from difficulty.maps.map import ObstacleMap
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.gate_obstacle import ObstacleGate
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.train_obstacle import ObstacleTrain
from entities.obstacles.impl.wooden_sign_obstacle import ObstacleWoodenSign
from entities.obstacles.impl.indicator_obstacle import ObstacleIndicator
from entities.obstacles.obstacle_metadata_factory import ObstacleFactory

@dataclass
class SecondObstacleMap(ObstacleMap):
    _big_obstacles: ObstacleFactory = field(default_factory=lambda: ObstacleFactory([
        {"obstacle": ObstacleLongCube, 'difficulty': 1, 'probability': 0.4, 'has_ladder': 0.9},
        {"obstacle": ObstacleTrain, 'difficulty': 1, 'probability': 0.4}],
        4))

    _small_obstacles: ObstacleFactory = field(default_factory=lambda: ObstacleFactory([
        # {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.1},
        # {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.05},
        {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.05, 'colorr': color.yellow},
        {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.05}],
        4))

    # _signs: ObstacleFactory = field(default_factory=lambda: ObstacleFactory([
    #     {"obstacle": ObstacleWoodenSign, 'difficulty': 1, 'probability': 0.1},
    #     {"obstacle": ObstacleIndicator, 'difficulty': 1, 'probability': 0.05}],
    #     5))

    # _gates: ObstacleFactory = field(default_factory=lambda: ObstacleFactory([
    #     {"obstacle": ObstacleGate, 'difficulty': 1, 'probability': 0.1}],
    #     1))

    obstacles: List = field(default_factory=list)
    lane_change_const: float = 0.2
    small_obstacle_const: float = 0.7

    def generate_obstacles(self, obstacle_generation_distance, start, length):
        last_obstacle_z = start + obstacle_generation_distance
        end = start + length
        start_x = random.randint(0, 1)

        self.obstacles = []
        while last_obstacle_z <= end:
            if random.random() < self.lane_change_const:
                if obstacle_generation_distance <= 150:
                    last_obstacle_z += obstacle_generation_distance

                start_x = int(not start_x)

            # self.__create_signs(z_position=last_obstacle_z-obstacle_generation_distance/2)
            # if random.random() < 0.3:
            #     self.__generate_gate(last_obstacle_z)
            # else:
            self.__create_trains(start_x, last_obstacle_z)
            self.__create_small_obstacles(int(not start_x), last_obstacle_z, self.small_obstacle_const)
            last_obstacle_z += obstacle_generation_distance
        return last_obstacle_z

    def __create_trains(self, start_x: int, z_position: float):
        for lane in range(start_x, LANE_COUNT, 2):
            self.obstacles.append(self._big_obstacles.create_obstacle(z_position, lane))

    # def __create_signs(self, z_position: float):
    #     self.obstacles.append(self._signs.create_obstacle(z_position, random.randint(0,LANE_COUNT)))
    #
    # def __generate_gate(self, z_position: float):
    #     self.obstacles.append(self._gates.create_obstacle(z_position, 0))

    def __create_small_obstacles(self, start_x: int, z_position: float, small_obstacle_const):
        for lane in range(start_x, LANE_COUNT, 2):
            if random.random() < small_obstacle_const:
                self.obstacles.append(self._small_obstacles.create_obstacle(z_position, lane))