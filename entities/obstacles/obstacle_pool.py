import copy
from collections import defaultdict, deque
from entities.obstacles.obstacle import Obstacle  # Base class of obstacles

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
                self.reusable_obstacles[obstacle_class].append(obstacle)

    def acquire(self, obstacle_class, position_z, difficulty, lane, metadata, *args, **kwargs) -> Obstacle:
        if self.reusable_obstacles[obstacle_class]:
            obstacle = self.reusable_obstacles[obstacle_class].pop()
            self.__set_obstacle_attr(obstacle, position_z=position_z, lane=lane, **metadata)
        else:
            obstacle = obstacle_class(position_z=position_z, difficulty=difficulty, lane=lane, **metadata)
        return obstacle

    def release(self, obstacle: Obstacle):
        obstacle_class = type(obstacle)
        if len(self.reusable_obstacles[obstacle_class]) < self.max_size_per_type:
            self.__set_obstacle_attr(obstacle, position_z=-1000, lane=0)
            self.reusable_obstacles[obstacle_class].append(obstacle)
        else:
            del obstacle

    def __set_obstacle_attr(self, obstacle: Obstacle, **kwargs):
        for key, value in kwargs.items():
            setter_name = f"set_{key}"
            if hasattr(obstacle, setter_name):
                getattr(obstacle, setter_name)(value)

