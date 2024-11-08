import copy
from collections import defaultdict, deque

from ursina import destroy

from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate

from entities.obstacles.obstacle import Obstacle


class ObstaclePool:
    def __init__(self, obstacle_types: list, max_size_per_type=100):
        self.max_size_per_type = max_size_per_type
        self.reusable_obstacles = defaultdict(deque)
        self.obstacle_types = obstacle_types
        self.__create_reusable_obstacles()

    def __create_reusable_obstacles(self):
        for obstacle_class in self.obstacle_types:
            for _ in range(1):
                obstacle = obstacle_class(position_z=-1000, difficulty=1)
                obstacle.visible = False
                obstacle.enabled = False
                for child in obstacle.children:
                    child.visible = False
                    child.enabled = False
                self.reusable_obstacles[obstacle_class].append(obstacle)

    def acquire(self, obstacle_class, position_z, difficulty, lane, metadata, *args, **kwargs) -> Obstacle:
        # if not (
        #         obstacle_class == ObstacleLongCube or obstacle_class == ObstaclePoleGate or obstacle_class == ObstacleBoard) and \
        #         self.reusable_obstacles[obstacle_class]:
        #     obstacle = self.reusable_obstacles[obstacle_class].pop()
        #     self.__set_obstacle_attr(obstacle, **metadata)
        #     obstacle.set_lane(lane)
        #     obstacle.set_position_z(position_z)
        #     obstacle.enabled = True
        #     for child in obstacle.children:
        #         child.enabled = True
        # else:
        obstacle = obstacle_class(position_z=position_z, difficulty=difficulty, lane=lane, **metadata)
        return obstacle

    def release(self, obstacle: Obstacle):
        obstacle_class = type(obstacle)
        if not (type(obstacle) == ObstacleLongCube or type(obstacle) == ObstaclePoleGate or type(
                obstacle) == ObstacleBoard) and len(self.reusable_obstacles[obstacle_class]) < self.max_size_per_type:
            # obstacle.set_position_z(-1000)
            obstacle.enabled = False
            for child in obstacle.children:
                child.enabled = False
            self.reusable_obstacles[obstacle_class].append(obstacle)
            print(f'release obstacle {self.reusable_obstacles}')
        else:
            print("delete")
            destroy(obstacle)
            obstacle.delete()
            del obstacle

    def __set_obstacle_attr(self, obstacle: Obstacle, **kwargs):
        for key, value in kwargs.items():
            setter_name = f"set_{key}"
            if hasattr(obstacle, setter_name):
                print(f'set {setter_name}, {value}')
                getattr(obstacle, setter_name)(value)
