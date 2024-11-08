from enum import Enum

from ursina import color

from config.constants import Color

class ColorTheme(Enum):
    COLOR_THEME_GREEN = {
        "ObstacleGate": Color.DARK_GREEN.get_color(),
        "ObstacleLongCube": Color.DARK_GREEN.get_color(),
        "ObstacleTrain": Color.DARK_GREEN.get_color(),
        "ObstacleFence": Color.DARK_GREEN.get_color(),
        "ObstacleBoard": Color.GRAY.get_color(),
        "ObstaclePoleGate": color.dark_gray,
        "ObstacleCube": Color.DARK_GREEN.get_color(),
        "ObstacleWoodenSign": Color.DARK_GREEN.get_color(),
        "ObstacleIndicator": Color.DARK_GREEN.get_color(),
    }


    COLOR_THEME_DARK = {
        "ObstacleGate": Color.DARK_BROWN.get_color(),
        "ObstacleLongCube": Color.DARK_GREEN.get_color(),
        "ObstacleTrain": Color.DARK_RED.get_color(),
        "ObstacleFence": Color.DARK_BROWN.get_color(),
        "ObstacleBoard": Color.GRAY.get_color(),
        "ObstaclePoleGate": color.dark_gray,
        "ObstacleCube": Color.DARK_GRAY.get_color(),
        "ObstacleWoodenSign": Color.DARK_BROWN.get_color(),
        "ObstacleIndicator": Color.DARK_GRAY.get_color(),
    }

    COLOR_THEME_COLORFULL = {
        "ObstacleGate": Color.RED.get_color(),
        "ObstacleLongCube": Color.YELLOW.get_color(),
        "ObstacleTrain": Color.RED.get_color(),
        "ObstacleFence": Color.BLUE.get_color(),
        "ObstacleBoard": Color.GRAY.get_color(),
        "ObstaclePoleGate": color.dark_gray,
        "ObstacleCube": Color.LIGHT_GREEN.get_color(),
        "ObstacleWoodenSign": Color.BROWN.get_color(),
        "ObstacleIndicator": Color.ORANGE.get_color(),
    }


    COLOR_THEME_BASIC = {
        "ObstacleGate": Color.BROWN.get_color(),
        "ObstacleLongCube": Color.GREEN.get_color(),
        "ObstacleTrain": Color.RED.get_color(),
        "ObstacleFence": Color.BROWN.get_color(),
        "ObstacleBoard": Color.GRAY.get_color(),
        "ObstaclePoleGate": color.dark_gray,
        "ObstacleCube": Color.RED.get_color(),
        "ObstacleWoodenSign": Color.BROWN.get_color(),
        "ObstacleIndicator": Color.BROWN.get_color(),
    }