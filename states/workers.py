import time

from difficulty.difficulty.impl.difficulty_level1 import Difficulty1
from difficulty.difficulty.impl.difficulty_level2 import Difficulty2
from difficulty.difficulty_manager import DifficultyManager


def obstacle_generator_worker(obstacle_queue, player_z, go, difficulty_level, mapp_data_queue, **kwargs):
    print("start generating")
    prev = difficulty_level.value
    difficulty_level_obj = Difficulty1()
    difficulty_manager = DifficultyManager()
    while go.value:
        obstacles, map_data = difficulty_level_obj.generate_obstacle(player_z.value)
        if obstacles:
            # print(f"addded obs {obstacles[0].position_z}, {obstacles[len(obstacles) - 1].position_z}")
            if prev != difficulty_level.value:
                difficulty_level_obj = difficulty_manager.change_level_class(difficulty_level.value, difficulty_level_obj)
                prev=difficulty_level.value

            if map_data[0]:
                mapp_data_queue.put(map_data)
            for obstacle in obstacles:
                print("put obstacle to queue")
                obstacle_queue.put(obstacle)
                time.sleep(0.1)