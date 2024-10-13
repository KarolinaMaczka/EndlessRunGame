class ObstacleFlyweight:
    def __init__(self, y_position: int, difficulty: int, **kwargs):
        self.entity_metadata = kwargs
        self.y_position = y_position
        self.difficulty = difficulty
        print(f"Created an obstacle flyweight with attributes: {kwargs}")
