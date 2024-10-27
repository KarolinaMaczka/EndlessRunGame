from ursina import Entity


class ObstacleMetaData:
    def __init__(self, difficulty: int, obstacle: Entity, probability: float = 0.5,  **kwargs):
        self.entity_metadata = kwargs
        self.probability = probability,
        self.difficulty = difficulty
        self.obstacle = obstacle
        print(f"Created an obstacle flyweight with attributes: {kwargs}")
