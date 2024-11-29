from copy import copy

from ursina import Entity, color, destroy

from config.constants import ROAD_HEIGHT, ROAD_WIDTH, LANE_WIDTH, Color
from config.utils import catch_exceptions


class Scenery:
    def __init__(self, models):
        final_width = ROAD_WIDTH + LANE_WIDTH
        final_width_walls = ROAD_WIDTH
        self.models = models

        self.right_wall = Entity(model=copy(models.cube_standard), texture='brick', collider='box',
                                 position=(final_width_walls + 0.2 // 2, 0, 0),
                                 always_on_top=1,
                                 scale=(0.1, 1000, 100000),
                                 color=Color.BEIGE.get_color())

        self.left_wall = Entity(model=copy(models.cube_standard), texture='brick', collider='box',
                                position=(-final_width_walls - 0.2 // 2, 0, 0),
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

    def delete(self):
        destroy(self.road)
        destroy(self.left_wall)
        destroy(self.right_wall)
