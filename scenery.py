from ursina import Entity, color

from config.constants import ROAD_HEIGHT


class Scenery:
    def __init__(self):
        self.road = Entity(model='plane', texture='grass', scale=(60, ROAD_HEIGHT, 1000000), color=color.dark_gray)
        self.right_grass = Entity(model='cube', texture='grass', collider='box', position=(60//2+500, 0, 0),
                                   scale=(1001, 2, 1000000),
                                   color=color.white)

        self.left_grass = Entity(model='cube', texture='grass', collider='box', position=(-60//2-500, 0, 0),
                                  scale=(1001, 2, 1000000),
                                  color=color.white)
