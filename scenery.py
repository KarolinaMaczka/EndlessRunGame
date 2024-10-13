from ursina import Entity, color


class Scenery:
    def __init__(self):
        self.road = Entity(model='plane', texture='grass', scale=(50, 10, 1000000), color=color.dark_gray)

        self.median_right = Entity(model='cube', texture='grass', collider='box', position=(25, 2, 0),
                                   scale=(5, 10, 1000000),
                                   color=color.white)

        self.median_left = Entity(model='cube', texture='grass', collider='box', position=(-25, 2, 0),
                                  scale=(5, 10, 1000000),
                                  color=color.white)
