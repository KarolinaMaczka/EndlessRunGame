import multiprocessing

from ursina import Ursina, window, Sky, Text

from config.logger import get_game_logger
from entities.camera import PlayerCamera
from game_manager import GameManager
from entities.player import Player
import atexit

from multiprocessing import Process, Queue, Manager
from camera_reading.read_camera import CameraReader
from data_manager import DataManager

if __name__ == '__main__':
    logger = get_game_logger()
    logger.info('Starting game')

    list_manager = Manager()
    data_manager = DataManager(list_manager)

    camera_reading = CameraReader(list_manager)

    atexit.register(camera_reading.on_exit)

    app = Ursina()

    window.fps_counter.enabled = True
    # window.exit_button.enabled = False
    # TODO fill
    window.title = 'Game'

    player = Player()

    camera = PlayerCamera(player)

    game_manager = GameManager(player, camera, data_manager, camera_reading)
    atexit.register(game_manager.on_exit)

    camera_reading.camera_ready_event.wait()
    logger.info('Camera process started')


    def update():
        game_manager.update()


    def input(key):
        game_manager.input(key)


    sky = Sky()

    app.run()
