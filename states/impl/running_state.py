from ursina import *

from config.logger import get_game_logger
from difficulty.difficulty.difficulty_levels import Difficulty1
from difficulty.difficulty_manager import DifficultyManager
from difficulty.difficulty_logic import DifficultyLogic

from entities.obstacles.obstacle_pool import ObstaclePool
from scenery import Scenery
from states.state import GameState
from collections import deque
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.gate_obstacle import ObstacleGate
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.indicator_obstacle import ObstacleIndicator
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.wooden_sign_obstacle import ObstacleWoodenSign
from entities.obstacles.impl.train_obstacle import ObstacleTrain

import multiprocessing
import atexit

from states.workers import obstacle_generator_worker
logger = get_game_logger()


class RunningState(GameState):
    def __init__(self, context):
        self.scenery = Scenery()
        self.active_obstacles = deque()
        self.obstacles_to_render = deque()
        self.obstacles_per_frame = 1
        self.context = context
        self.cleanup_threshold = 200
        self.obstacle_pool = ObstaclePool([
            ObstacleFence,
            ObstacleGate,
            ObstaclePoleGate,
            ObstacleBoard,
            ObstacleCube,
            ObstacleIndicator,
            ObstacleLongCube,
            ObstacleWoodenSign,
            ObstacleTrain
        ], max_size_per_type=15)
        self.difficulty_manager = DifficultyManager()
        self.difficulty_level = multiprocessing.Value('i', 1)
        self.difficulty_level_new = multiprocessing.Value('i', 1)
        self.go = multiprocessing.Value('b', True)
        self.player_z = multiprocessing.Value('d', 0.0)
        self.obstacle_queue = multiprocessing.Queue()
        self.map_data_queue = multiprocessing.Queue()
        self.obstacle_process = multiprocessing.Process(
            target=obstacle_generator_worker,
            args=(self.obstacle_queue, self.player_z, self.go, self.difficulty_level, self.map_data_queue)
        )
        self.obstacle_process.start()
        self.difficulty_logic = DifficultyLogic(self.context.data_manager, self.difficulty_level_new)
        self.logic_process = multiprocessing.Process(target=self.difficulty_logic.update, args=(self.player_z, self.context.emotion_queue))
        self.logic_process.start()
        self.start()
        self.create_paused_panel()

    def on_exit(self):
        for obstacle in self.active_obstacles:
            obstacle.delete()
            destroy(obstacle)
        self.active_obstacles.clear()
        logger.info(f'Cleaned obstacles')
        self.go.value = False
        if hasattr(self, "obstacle_process"):
            self.obstacle_process.terminate()
            self.obstacle_process.join()
            del self.obstacle_process
            logger.info(f'Deleted obstacle process')
        if hasattr(self, "logic_process"):
            self.logic_process.terminate()
            self.logic_process.join()
            del self.logic_process
            logger.info(f'Deleted logic process')
        self.scenery.delete()

    def handle_input(self):
        self.context.player.reset()
        if held_keys['d']:
            self.context.player.go_right()
            self.context.data_manager.save_pressed_key(('d', self.player_z.value))
        if held_keys['a']:
            self.context.player.go_left()
            self.context.data_manager.save_pressed_key(('a', self.player_z.value))
        # if held_keys['w']:
        #     self.context.player.run_faster()
        if held_keys['s']:
            self.context.player.crouch()
            # self.context.player.scale = 3.5
            self.context.camera.camera.y = self.context.camera.camera.y - 0.3
            self.context.data_manager.save_pressed_key(('s', self.player_z.value))
        if held_keys['escape']:
            self.__toggle_paused()
        if held_keys['control']:
            for i in range(10):
                if held_keys[str(i)]:
                    self.set_difficulty(max(1, min(10, i+1)))
        if held_keys['space'] and not self.context.player.is_jumping:
            self.context.player.set_jump()
            self.context.data_manager.save_pressed_key(('space', self.player_z.value))

    def start(self):
        self.context.player.set_values()
        self.context.player.visible = True
        for obstacle in self.active_obstacles:
            obstacle.delete()
            destroy(obstacle)
        self.active_obstacles.clear()
        self.__initialize_obstacles()
        self.context.data_manager.save_difficulty(self.difficulty_level.value)
        atexit.register(self.on_exit)
        
    def update(self):
        if self.difficulty_level.value != self.difficulty_level_new.value:
            self.set_difficulty(self.difficulty_level_new.value)
        self.context.player.run()
        self.handle_input()
        self.context.physics_engine.apply_gravity(self.active_obstacles)
        if self.context.physics_engine.handle_player_collisions():
            self.context.transition_to("game_over_state")
            return
        self.player_z.value = self.context.player.z
        self.__render_obstacles_from_queue()
        self.__cleanup_obstacles()
        self.__save_mapp_data()
        self.scenery.move(self.context.player.z)

    def create_paused_panel(self):
        self.pause_panel = WindowPanel(
            title='Resume',
            content=(
                Button('Resume', color=color.gray, on_click=self.__toggle_paused),
                Button('Main Menu', color=color.gray, on_click=self.__transition_to_main_menu),
                Button('Quit', color=color.red, on_click=application.quit)
            ),
            position=(0, 0.25),
            enabled=False
        )

    def set_difficulty(self, level, **kwargs):
        logger.info(f'RunningState setting difficulty to {level}')
        self.difficulty_level.value = level
        self.difficulty_manager.set_player_settings(level, self.context.player)
        self.context.data_manager.save_difficulty(level)

    def __toggle_paused(self):
        if not application.paused:
            logger.info('Pausing game')
        else:
            logger.info('Resuming game')
        application.paused = not application.paused
        self.pause_panel.enabled = application.paused

    def __save_mapp_data(self):
        while not self.map_data_queue.empty():
            logger.info('Saving mapp data')
            mapp_data = self.map_data_queue.get()
            self.context.data_manager.add_map_data(mapp_data)

    def __transition_to_main_menu(self):
        logger.info('Transitioning to main menu')
        self.__toggle_paused()
        self.on_exit()
        self.context.transition_to('main_menu')

    def __initialize_obstacles(self):
        logger.info('initializing objects')
        obstacles, mapp_data = Difficulty1().initialize_obstacles()
        self.context.data_manager.add_map_data(mapp_data)
        for obstacle_type in obstacles:
            self.context.data_manager.add_obstacle_data(obstacle_type=obstacle_type)
            obstacle = self.obstacle_pool.acquire(obstacle_type.obstacle, position_z=obstacle_type.position_z,
                                                  difficulty=obstacle_type.difficulty, lane=obstacle_type.lane,
                                                  metadata=obstacle_type.entity_metadata)

            # obstacle = obstacle_type.obstacle(obstacle_type.position_z, obstacle_type.difficulty, obstacle_type.lane)
            self.active_obstacles.append(obstacle)

    def __cleanup_obstacles(self):
        player_z = self.context.player.z
        obstacles_to_remove = []
        for obstacle in list(self.active_obstacles):
            if obstacle.z < player_z - self.cleanup_threshold:
                logger.info(f'Adding obstacles to remove to the stack: obstacle.z {obstacle.z}, player.z {player_z}')
                obstacles_to_remove.append(obstacle)

        for obstacle in obstacles_to_remove:
            self.active_obstacles.remove(obstacle)
            obstacle.delete()
            destroy(obstacle)
            # self.obstacle_pool.release(obstacle)
        obstacles_to_remove.clear()

    def __render_obstacles_from_queue(self):
        for _ in range(self.obstacles_per_frame):
            if self.obstacle_queue.empty():
                break
            logger.info(f'Rendering obstacles from queue')
            obstacle_type = self.obstacle_queue.get()
            # obstacle = obstacle_type.obstacle(obstacle_type.position_z, obstacle_type.difficulty, obstacle_type.lane)
            obstacle = self.obstacle_pool.acquire(
                obstacle_type.obstacle,
                position_z=obstacle_type.position_z,
                difficulty=obstacle_type.difficulty,
                lane=obstacle_type.lane,
                metadata=obstacle_type.entity_metadata
            )
            self.active_obstacles.append(obstacle)
            self.context.data_manager.add_obstacle_data(obstacle_type=obstacle_type)
