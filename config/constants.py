from enum import Enum

INITIAL_FIRST_OBSTACLE_Z_POS = 500
INITIAL_LAST_OBSTACLE_Z_POS = 2500

BOUNCE_DIST = 2  # Distance difference after collision
SLIGHT_BOUNCE_DIST = 3  # Small distance difference after slight collision
COLLISION_DIST = 3  # Distance from obstacle so that collision is marked as a full collision
SLIGHT_COLLISION_DIST = 2  # Distance from obstacle so that collision is marked as a slight collision
ROAD_WIDTH = 50
ROAD_HEIGHT = 2
LANE_WIDTH = 10
STANDARD_OBSTACLE_HEIGHT = 10


class CollisionType(Enum):
    LIGHT = "light"
    FULL = "full"


class CollisionSide(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
