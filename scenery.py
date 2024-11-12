from ursina import Entity, color, destroy

from config.constants import ROAD_HEIGHT, ROAD_WIDTH, LANE_WIDTH, Color
from config.utils import catch_exceptions


class Scenery:
    def __init__(self):
        final_width = ROAD_WIDTH + LANE_WIDTH
        final_width2 = ROAD_WIDTH

        # self.right_grass = Entity(model='cube', texture='grass', collider='box',
        #                           position=(final_width // 2 + 500, 0, 0),
        #                           always_on_top=1,
        #                           scale=(1001, 2, 100000),
        #                           color=color.white)
        #
        # self.left_grass = Entity(model='cube', texture='grass', collider='box',
        #                          position=(-final_width // 2 - 500, 0, 0),
        #                          scale=(1001, 2, 100000),
        #                          always_on_top=1,
        #                          color=color.white)

        self.right_wall = Entity(model='cube', texture='brick', collider='box',
                                 position=(final_width2 + 0.2 // 2, 0, 0),
                                 always_on_top=1,
                                 scale=(0.1, 1000, 100000),
                                 color=Color.BEIGE.get_color())

        self.left_wall = Entity(model='cube', texture='brick', collider='box',
                                position=(-final_width2 - 0.2 // 2, 0, 0),
                                scale=(0.1, 1000, 100000),
                                always_on_top=1,
                                color=Color.BEIGE.get_color())

        self.road = Entity(model='plane', texture='grass', scale=(final_width, ROAD_HEIGHT, 100000),
                           color=color.dark_gray, always_on_top=1)

    @catch_exceptions
    def move(self, player_z):
        if player_z > self.road.z:
            self.road.z = player_z + 4500
            self.left_wall.z = player_z + 4500
            self.right_wall.z = player_z + 4500
            # self.right_grass.z = player_z + 4500
            # self.left_grass.z = player_z + 4500

    def delete(self):
        destroy(self.road)
        destroy(self.left_wall)
        destroy(self.right_wall)
        # destroy(self.right_grass)
        # destroy(self.left_grass)
