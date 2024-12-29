from enum import Enum

from ursina import color

INITIAL_FIRST_OBSTACLE_Z_POS = 500
INITIAL_LAST_OBSTACLE_Z_POS = 3500

# BOUNCE_DIST = 2  # Distance difference after collision
# SLIGHT_BOUNCE_DIST = 3  # Small distance difference after slight collision
# COLLISION_DIST = 3  # Distance from obstacle so that collision is marked as a full collision
# SLIGHT_COLLISION_DIST = 2  # Distance from obstacle so that collision is marked as a slight collision
ROAD_WIDTH = 30
ROAD_HEIGHT = 2
LANE_WIDTH = 10
STANDARD_OBSTACLE_HEIGHT = 10
LANE_COUNT = 3


class CollisionType(Enum):
    LIGHT = "light"
    FULL = "full"


class CollisionSide(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Color(Enum):
    BEIGE = "#fff5d8"
    LIGHT_GREEN = "#93c47d"
    GREEN = "#335802"
    DARK_GREEN = "#0c343d"
    BROWN = "#5b3610"
    DARK_BROWN = "#482b0d"
    GRAY = "#bcbcbc"
    DARK_GRAY = "#444444"
    RED = "#cc0000"
    DARK_RED = "#482b0d"
    YELLOW = "#f1c232"
    DARK_YELLOW = "#bf9000"
    BLUE = "#3d85c6"
    DARK_BLUE = "#16537e"
    PINK = "#c90076"
    PURPLE = "#674ea7"
    ORANGE = "#e69138"

    def get_color(self):
        return color.hex(self.value)
