from ursina import Ursina, color

from entities.obstacles.custom_dictionary import CustomDictionary
from entities.obstacles.obstacle_flyweight import ObstacleFlyweight
import random


class ObstacleFlyweightFactory:
    _obstacles: CustomDictionary[str, ObstacleFlyweight]

    def __init__(self, init_obstacles: list[dict]):
        self._obstacles = CustomDictionary()
        for obstacle_type in init_obstacles:
            self._obstacles[obstacle_type] = ObstacleFlyweight(**obstacle_type)

    def get_obstacle(self, obstacle_desc: dict) -> ObstacleFlyweight:
        try:
            self._obstacles[obstacle_desc]
        except KeyError:
            self._obstacles[obstacle_desc] = ObstacleFlyweight(**obstacle_desc)
        finally:
            return self._obstacles[obstacle_desc]

    def list_obstacles(self):
        print(', '.join(key for key, _ in self._obstacles.items()))

    def get_random(self) -> ObstacleFlyweight:
        return random.choice(list(self._obstacles.values()))


if __name__ == '__main__':
    app = Ursina()
    factory = ObstacleFlyweightFactory([
        {'color': color.red, 'collider': 'box', 'scale': (3.5, 3.5, 3.5), "y_position": 2, 'difficulty': 1},
        {'color': color.blue, 'collider': 'box', 'scale': (3.5, 3.5, 3.5), "y_position": 2, 'difficulty': 1}
    ])

    factory.list_obstacles()

    obstacle = factory.get_obstacle({'color': color.red, 'collider': 'box', 'scale': (3.5, 3.5, 3.5), "y_position": 2, 'difficulty': 1})
    obstacle1 = factory.get_obstacle({'color': color.blue, 'collider': 'box', 'scale': (3.5, 3.5, 3.5), "y_position": 2, 'difficulty': 1})
    print(obstacle1)
    print("random")
    obs2 = factory.get_random()
    print(obs2)
