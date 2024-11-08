from ursina import *

from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.difficulty.impl.difficulty_level1 import Difficulty1
from difficulty.difficulty.impl.difficulty_level2 import Difficulty2
from difficulty.difficulty_manager import DifficultyManager
from datetime import datetime

from entities.obstacles.obstacle_pool import ObstaclePool
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
from camera_reading.read_camera import EmotionHolder

import multiprocessing

from states.workers import obstacle_generator_worker


class RunningState(GameState):
    def __init__(self, context):
        self.is_game_over = False
        self.difficulty_class_level = Difficulty1()
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
        self.go = multiprocessing.Value('b', True)
        self.player_z = multiprocessing.Value('d', 0.0)
        self.obstacle_queue = multiprocessing.Queue()
        self.map_data_queue = multiprocessing.Queue()
        self.obstacle_process = multiprocessing.Process(
            target=obstacle_generator_worker,
            args=(self.obstacle_queue, self.player_z, self.go, self.difficulty_level, self.map_data_queue)
        )
        self.obstacle_process.start()
        self.start()
        self.create_paused_panel()

    def on_exit(self):
        for obstacle in self.active_obstacles:
            obstacle.delete()
            destroy(obstacle)
        self.active_obstacles.clear()
        print('exiting state')
        self.go.value = False
        if hasattr(self, "obstacle_process"):
            self.obstacle_process.terminate()
            self.obstacle_process.join()
            del self.obstacle_process

    def handle_input(self):
        self.context.player.reset()
        if held_keys['d']:
            self.context.player.go_right()
        if held_keys['a']:
            self.context.player.go_left()
        # if held_keys['w']:
        #     self.context.player.run_faster()
        if held_keys['s']:
            self.context.player.crouch()
            # self.context.player.scale = 3.5
            self.context.camera.camera.y = self.context.camera.camera.y - 0.3
        if held_keys['l']:
            self.set_difficulty(1)
        if held_keys['escape']:
            self.__toggle_paused()
        if held_keys['h']:
            self.set_difficulty(2)
        if held_keys['space'] and not self.context.player.is_jumping:
            self.context.player.set_jump()

    def start(self):
        self.context.player.z = 0
        self.context.player.visible = True

        for obstacle in self.active_obstacles:
            obstacle.delete()
            destroy(obstacle)
        self.active_obstacles.clear()
        self.__initialize_obstacles()

    def update(self):
        if self.is_game_over:
            return
        self.context.player.run()
        self.handle_input()
        self.context.physics_engine.apply_gravity(self.active_obstacles)
        if self.context.physics_engine.handle_player_collisions():
            self.context.transition_to("game_over_state")
        self.player_z.value = self.context.player.z
        self.__render_obstacles_from_queue()
        self.__cleanup_obstacles()
        self.__save_mapp_data()

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
        self.difficulty_level.value = level
        self.difficulty_manager.set_player_settings(level, self.context.player)

    def __toggle_paused(self):
        application.paused = not application.paused
        self.pause_panel.enabled = application.paused

    def __save_mapp_data(self):
        while not self.map_data_queue.empty():
            mapp_data = self.map_data_queue.get()
            self.context.data_manager.save_map_data(mapp_data)

    def __transition_to_main_menu(self):
        self.__toggle_paused()
        self.on_exit()
        self.context.transition_to('main_menu')

    def __initialize_obstacles(self):
        obstacles, mapp_data = self.difficulty_class_level.initialize_obstacles()
        self.context.data_manager.save_map_data(mapp_data)
        for obstacle_type in obstacles:
            self.context.data_manager.save_obstacle_data(obstacle_type=obstacle_type)
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
                print(f'remove obst {obstacle.z}, player {player_z}')
                obstacles_to_remove.append(obstacle)

        for obstacle in obstacles_to_remove:
            print(self.active_obstacles)
            self.active_obstacles.remove(obstacle)
            print(f'after removing {self.active_obstacles}')
            obstacle.delete()
            destroy(obstacle)
            # self.obstacle_pool.release(obstacle)
        obstacles_to_remove.clear()

    def __render_obstacles_from_queue(self):
        for _ in range(self.obstacles_per_frame):
            if self.obstacle_queue.empty():
                break
            print(f'not empty queue')
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
            self.context.data_manager.save_obstacle_data(obstacle_type=obstacle_type)
            print(f'after adding {self.active_obstacles}')
