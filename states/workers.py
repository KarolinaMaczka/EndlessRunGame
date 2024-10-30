import time

from difficulty.difficulty.impl.difficulty_level1 import Difficulty1
from difficulty.difficulty.impl.difficulty_level2 import Difficulty2
from difficulty.difficulty_manager import DifficultyManager


def obstacle_generator_worker(obstacle_queue, player_z, go, difficulty_level, **kwargs):
    prev = difficulty_level.value
    difficulty_level_obj = Difficulty1()
    difficulty_manager = DifficultyManager()
    while go.value:
        obstacles = difficulty_level_obj.generate_obstacle(player_z.value)
        if obstacles:
            print(f"addded obs {obstacles[0].position_z}, {obstacles[len(obstacles) - 1].position_z}")
            if prev != difficulty_level.value:
                difficulty_level_obj = difficulty_manager.change_level_class(difficulty_level.value, difficulty_level_obj)
                prev=difficulty_level.value

            for obstacle in obstacles:
                obstacle_queue.put(obstacle)
                time.sleep(0.06)