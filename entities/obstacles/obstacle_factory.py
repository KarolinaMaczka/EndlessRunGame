from entities.obstacles.obstacle import Obstacle
from entities.obstacles.obstacle_flyweight_factory import ObstacleFlyweightFactory


class ObstacleFactory:
    def __init__(self, available_obstacles):
        self.available_obstacles: ObstacleFlyweightFactory = available_obstacles

    def create_obstacle(self, position_x: float, position_z: float) -> Obstacle:
        obstacle_type = self.available_obstacles.get_random()
        return Obstacle(obstacle_type, position_x, position_z)
