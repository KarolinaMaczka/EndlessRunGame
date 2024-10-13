from ursina import color

from entities.obstacles.obstacle_flyweight_factory import ObstacleFlyweightFactory


class Difficulty:
    def __init__(self):
        self.available_obstacles = ObstacleFlyweightFactory([
            {'color': color.red, 'collider': 'box', 'scale': (3.5, 3.5, 3.5)},
            {'color': color.blue, 'collider': 'box', 'scale': (3.5, 3.5, 3.5)}
        ])
        self.obstacle_generation_distance = 100
