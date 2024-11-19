# import time
#
# from config.logger import get_game_logger
# from difficulty.difficulty_manager import DifficultyManager
#
# logger = get_game_logger()
#
# def obstacle_generator_worker(obstacle_queue, player_z, go, difficulty_level, mapp_data_queue, **kwargs):
#     logger.info(f'Start generating obstacles')
#     prev = difficulty_level.value
#     logger.info(f'Difficulty level {prev}')
#     difficulty_manager = DifficultyManager()
#     difficulty_level_obj = difficulty_manager.difficulties.get(difficulty_level.value)
#     while go.value:
#         obstacles, map_data = difficulty_level_obj.generate_obstacle(player_z.value)
#         if obstacles:
#             logger.info(f'worker - Difficulty level obj {difficulty_level_obj}')
#             logger.info(f'Putting obstacles in range {obstacles[0].position_z} - {obstacles[len(obstacles) - 1].position_z} to the queue')
#             if prev != difficulty_level.value:
#                 logger.info(f'Changing difficulty level from {prev} to {difficulty_level.value}')
#                 difficulty_level_obj = difficulty_manager.change_level_class(difficulty_level.value, difficulty_level_obj)
#                 prev = difficulty_level.value
#                 logger.info(f'Changed difficulty level to {type(difficulty_level_obj).__name__}')
#
#             if map_data:
#                 mapp_data_queue.put(map_data)
#
#             for obstacle in obstacles:
#                 obstacle_queue.put(obstacle)
#                 time.sleep(0.1)