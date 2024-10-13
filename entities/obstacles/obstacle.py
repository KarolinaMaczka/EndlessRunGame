from ursina import Entity

from entities.obstacles.obstacle_flyweight import ObstacleFlyweight


class Obstacle(Entity):
    def __init__(self, obstacle_flyweight: ObstacleFlyweight, position_x: float, position_z: float):
        super().__init__(**obstacle_flyweight.entity_metadata,
                         position=(position_x, obstacle_flyweight.y_position, position_z))
        print(f"Created an obstacle at position.z {position_z}")
