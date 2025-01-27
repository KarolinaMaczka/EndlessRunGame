import multiprocessing
import time

from config.logger import get_game_logger
from difficulty.difficulty_manager import DifficultyManager
from states.process_managers.process_manager import ProcessManager

logger = get_game_logger()


class ObstacleProcesManager(ProcessManager):
    def __init__(self, selected_difficulty_level):
        super().__init__()
        self.obstacle_queue = multiprocessing.Queue()
        self.map_data_queue = multiprocessing.Queue()
        self.player_z = multiprocessing.Value('d', 0.0)
        self.go = multiprocessing.Value('b', True)
        self.difficulty_level = multiprocessing.Value('i', selected_difficulty_level)
        # self.process_ready_event = multiprocessing.Event()
        self.process = multiprocessing.Process(
            target=self.obstacle_generator_worker,
            args=(self.obstacle_queue, self.player_z, self.go, self.difficulty_level, self.map_data_queue)
        )
        self.process.start()

    def obstacle_generator_worker(self, obstacle_queue, player_z, go, difficulty_level, mapp_data_queue, **kwargs):
        logger.info(f'Start generating obstacles')
        prev = difficulty_level.value
        logger.info(f'Difficulty level {prev}')
        difficulty_manager = DifficultyManager()
        difficulty_level_obj = difficulty_manager.difficulties.get(difficulty_level.value)
        while go.value:
            obstacles, map_data = difficulty_level_obj.generate_obstacle(player_z.value)
            if obstacles:
                logger.info(f'worker - Difficulty level obj {type(difficulty_level_obj).__name__}')
                logger.info(
                    f'Putting obstacles in range {obstacles[0].position_z} - {obstacles[len(obstacles) - 1].position_z} to the queue')
                if prev != difficulty_level.value:
                    logger.info(
                        f'Changing difficulty level from {prev} to {difficulty_level.value}')
                    difficulty_level_obj = difficulty_manager.change_level_class(
                        difficulty_level.value, difficulty_level_obj)
                    prev = difficulty_level.value
                    logger.info(
                        f'Changed difficulty level to {type(difficulty_level_obj).__name__}')

                if map_data:
                    mapp_data_queue.put(map_data)

                for obstacle in obstacles:
                    obstacle_queue.put(obstacle)
                    time.sleep(0.2)

    def on_exit(self):
        self.go.value = False
        super().on_exit()
        logger.info(f'Deleted obstacle process')
