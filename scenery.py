from ursina import Entity, color

from config.constants import ROAD_HEIGHT, ROAD_WIDTH, LANE_WIDTH, Color




class Scenery:
    def __init__(self):
        final_width = ROAD_WIDTH + LANE_WIDTH
        final_width2 = ROAD_WIDTH

        self.right_grass = Entity(model='cube', texture='grass', collider='box',
                                  position=(final_width // 2 + 500, 0, 0),
                                  always_on_top=1,
                                  scale=(1001, 2, 1000000),
                                  color=color.white)

        self.left_grass = Entity(model='cube', texture='grass', collider='box',
                                 position=(-final_width // 2 - 500, 0, 0),
                                 scale=(1001, 2, 1000000),
                                 always_on_top=1,
                                 color=color.white)

        self.right_wall = Entity(model='cube', texture='brick', collider='box',
                                 position=(final_width2+0.2 // 2, 0, 0),
                                 always_on_top=1,
                                 scale=(0.1, 1000, 1000000),
                                 color=Color.BEIGE.get_color())

        self.left_wall = Entity(model='cube', texture='brick', collider='box',
                                position=(-final_width2-0.2 // 2, 0, 0),
                                scale=(0.1, 1000, 1000000),
                                always_on_top=1,
                                color=Color.BEIGE.get_color())

        self.road = Entity(model='plane', texture='grass', scale=(final_width, ROAD_HEIGHT, 1000000), color=color.dark_gray, always_on_top=1)



