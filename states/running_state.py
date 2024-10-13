import random

from ursina import held_keys, destroy, color

from config.constants import INITIAL_LAST_OBSTACLE_Z_POS, INITIAL_FIRST_OBSTACLE_Z_POS
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.obstacle_factory import ObstacleFactory
from entities.obstacles.obstacle_flyweight_factory import ObstacleFlyweightFactory
from states.state import GameState


class RunningState(GameState):
    def __init__(self, context):
        self.is_game_over = False
        self.first_obstacle = INITIAL_FIRST_OBSTACLE_Z_POS
        self.obstacle_flyweight_factory = ObstacleFlyweightFactory([
            {"model": 'assets/container/12281_Container_v2_L2.obj',
             "scale": 0.01, "texture": 'assets/container/12281_Container_diffuse.jpg',
             "rotation": (90, 0, 0), "double_sided": True, 'y_position': 4, 'difficulty': 1},
            {"model": 'cube', "color": color.red, "collider": 'box',
             "scale": (3.5, 3.5, 3.5), "y_position": 2, 'difficulty': 1}
        ])
        self.obstacle_factory = ObstacleFactory(self.obstacle_flyweight_factory)
        self.last_obstacle_z = INITIAL_LAST_OBSTACLE_Z_POS
        self.obstacle_generation_distance = 100
        self.active_obstacles = []
        self.context = context
        self.start()

    def handle_input(self):
        if held_keys['d']:
            self.context.player.go_right()
        if held_keys['a']:
            self.context.player.go_left()
        if held_keys['w']:
            self.context.player.run_faster()
        if held_keys['space'] and not self.context.player.is_jumping:
            self.context.player.set_jump()

    def start(self):
        self.context.player.z = 0
        self.context.player.visible = True

        for obstacle in self.active_obstacles:
            destroy(obstacle)
        self.active_obstacles.clear()
        self.last_obstacle_z = INITIAL_LAST_OBSTACLE_Z_POS
        self.__initialize_obstacles()

    def update(self):
        if self.is_game_over:
            return

        self.context.player.run()
        self.__generate_obstacle()
        self.handle_input()
        self.context.physics_engine.apply_gravity()
        if self.context.physics_engine.handle_player_collisions(self.active_obstacles):
            self.context.transition_to("game_over_state")

    def __generate_obstacle(self):
        if self.context.player.z > self.first_obstacle + 200:
            spawn_z_position = self.last_obstacle_z + self.obstacle_generation_distance
            print(f"generating obstacle, z={self.context.player.z}, spawn.z = {spawn_z_position}")
            obstacle = self.obstacle_factory.create_obstacle(random.uniform(-10, 10), spawn_z_position)
            self.__add_obstacle(obstacle)
            self.__delete_passed_obstacle()

    def __add_obstacle(self, obstacle: Obstacle):
        self.active_obstacles.append(obstacle)
        self.last_obstacle_z += self.obstacle_generation_distance

    def __delete_passed_obstacle(self):
        old_obstacle = self.active_obstacles.pop(0)
        self.first_obstacle = old_obstacle.position.z
        destroy(old_obstacle)

    def __initialize_obstacles(self):
        for i in range(INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS, self.obstacle_generation_distance):
            obstacle = self.obstacle_factory.create_obstacle(random.uniform(-10, 10), i)
            self.active_obstacles.append(obstacle)


