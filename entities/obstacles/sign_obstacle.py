from ursina import invoke

from entities.obstacles.obstacle import Obstacle


class ObstacleSign(Obstacle):
    def __init__(self, position_z: float, difficulty: int, lane: int = 0, height: float = 0,
                 width: float = 0, depth: float = 0):
        super().__init__(position_z=position_z, difficulty=difficulty, lane=lane, height=height, width=width, depth=depth)
        self.lane = lane

    @staticmethod
    def set_fixed_lane(obj, lane):
        obj.x = -25 + lane * 10

    def set_lane(self, lane):
        self.lane = lane
        for child in self.children:
            invoke(self.set_fixed_lane, child, self.lane)