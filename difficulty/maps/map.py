from dataclasses import dataclass
from abc import ABC, abstractmethod

import random
from dataclasses import dataclass, field
from typing import List

from config.constants import LANE_COUNT, Color
from difficulty.maps.color_themes import ColorTheme
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.gate_obstacle import ObstacleGate
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.train_obstacle import ObstacleTrain
from entities.obstacles.impl.wooden_sign_obstacle import ObstacleWoodenSign
from entities.obstacles.impl.indicator_obstacle import ObstacleIndicator
from entities.obstacles.obstacle_metadata_factory import ObstacleMetadataFactory


@dataclass
class ObstacleMap(ABC):
    _big_obstacles: ObstacleMetadataFactory = field(default_factory=lambda: ObstacleMetadataFactory([
        {"obstacle": ObstacleLongCube, 'difficulty': 1, 'probability': 0.5, "has_ladder": 0.5},
        {"obstacle": ObstacleTrain, 'difficulty': 1, 'probability': 0.5}],
        4))

    _small_obstacles: ObstacleMetadataFactory = field(default_factory=lambda: ObstacleMetadataFactory([
        {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.3},
        {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.2},
        {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.3},
        {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.2}],
        4))

    _signs: ObstacleMetadataFactory = field(default_factory=lambda: ObstacleMetadataFactory([
        {"obstacle": ObstacleWoodenSign, 'difficulty': 1, 'probability': 0.5},
        {"obstacle": ObstacleIndicator, 'difficulty': 1, 'probability': 0.5}],
        5))

    _gates: ObstacleMetadataFactory = field(default_factory=lambda: ObstacleMetadataFactory([
        {"obstacle": ObstacleGate, 'difficulty': 1, 'probability': 0.1}],
        1))

    obstacles: List = field(default_factory=list)
    lane_change_const: float = 0.2
    small_obstacle_const: float = 0.7
    big_obstacle_const: float = 1.0
    gate_generation_const: float = 0.3
    obstacle_generation_distance: int = 200
    color_theme: ColorTheme = field(default_factory=lambda: ColorTheme.COLOR_THEME_BASIC)
    

    def get_metadata(self, first_obstacle, last_obstacle_z):
        return MapMetadata(self, first_obstacle, last_obstacle_z)

    @abstractmethod
    def generate_obstacles(self, start, length):
        pass

    def __post_init__(self):
        self._create_factories()
        self.apply_color_palette()

    def set_big_obstacles(self, obstacles) -> None:
        self._big_obstacles = obstacles
        self._big_obstacles.apply_color_palette(self.color_theme.value)

    def set_small_obstacles(self, obstacles) -> None:
        self._small_obstacles = obstacles
        print(self.color_theme.value)
        self._small_obstacles.apply_color_palette(self.color_theme.value)

    def apply_color_palette(self):
        for factory in self._factories:
            factory.apply_color_palette(self.color_theme.value)

    def _create_factories(self):
        self._factories = [self._gates, self._signs, self._big_obstacles, self._small_obstacles]

    def _create_trains(self, start_x: int, z_position: float, train_probability=1):
        for lane in range(start_x, LANE_COUNT, 2):
            if random.random() < train_probability:
                self.obstacles.append(self._big_obstacles.create_obstacle(z_position, lane))

    def _create_signs(self, z_position: float):
        self.obstacles.append(self._signs.create_obstacle(z_position, random.randint(0, LANE_COUNT)))

    def _generate_gate(self, z_position: float):
        z_position = self._adjust_last_position(z_position)
        self.obstacles.append(self._gates.create_obstacle(z_position, 0))
        return self._adjust_last_position(z_position)

    def _create_small_obstacles(self, start_x: int, z_position: float, small_obstacle_const):
        for lane in range(start_x, LANE_COUNT, 2):
            if random.random() < small_obstacle_const:
                self.obstacles.append(self._small_obstacles.create_obstacle(z_position, lane))

    def _adjust_last_position(self, last_obstacle_z):
        if self.obstacle_generation_distance <= 150:
            last_obstacle_z += self.obstacle_generation_distance
        return last_obstacle_z


class MapMetadata:
    def __init__(self, mapp: ObstacleMap, first_obstacle: float, last_obstacle_z: float):
        self.name = type(mapp).__name__
        self.lane_change_const = mapp.lane_change_const
        self.small_obstacle_const = mapp.small_obstacle_const
        self.gate_generation_const = mapp.gate_generation_const
        self.color_theme = mapp.color_theme.name
        self.first_obstacle = first_obstacle
        self.last_obstacle = last_obstacle_z
        self.obstacle_generation_distance = mapp.obstacle_generation_distance

