from config.constants import ROAD_WIDTH, LANE_WIDTH


def left_outer_border_lane(lane):
    return -ROAD_WIDTH / 2 + LANE_WIDTH * lane - 1


def left_inner_border_lane(lane):
    return -ROAD_WIDTH / 2 + LANE_WIDTH * lane + 1


def right_inner_border_lane(lane):
    return -ROAD_WIDTH / 2 + LANE_WIDTH * (lane + 1) - 1


def right_outer_border_lane(lane):
    return -ROAD_WIDTH / 2 + LANE_WIDTH * (lane + 1) + 1


def right_border_lane(lane):
    return -ROAD_WIDTH / 2 + LANE_WIDTH * (lane + 1)

def left_border_lane(lane):
    return -ROAD_WIDTH / 2 + LANE_WIDTH * lane
