import multiprocessing
import os

from ursina import Ursina, window, Sky

from config.logger import get_game_logger
from config.utils import set_window_on_top
from entities.camera import PlayerCamera
from entities.obstacles.Models import Models
from game_manager import GameManager
from entities.player import Player
import atexit

from multiprocessing import Manager
from states.process_managers.impl.read_camera import CameraReader
from data_manager import DataManager
from panda3d.core import Multifile
from panda3d.core import StringStream, Loader, Filename, PNMImage, Texture, VirtualFileSystem

if __name__ == '__main__':

    os.environ['DEEPFACE_HOME'] = os.path.join(os.getcwd(), 'deepface')
    multiprocessing.freeze_support()
    logger = get_game_logger()
    logger.info('Starting game')

    list_manager = Manager()
    data_manager = DataManager()

    camera_reading = CameraReader(list_manager)

    atexit.register(camera_reading.on_exit)

    app = Ursina()
    window.title = 'Game'
    window.fps_counter.enabled = True

    player = Player()
    camera = PlayerCamera(player)

    models = Models(app)

    game_manager = GameManager(player, camera, data_manager, camera_reading, models)
    atexit.register(game_manager.on_exit)

    camera_reading.camera_ready_event.wait()
    set_window_on_top("Game")
    logger.info('Camera process started')

    def update():
        game_manager.update()


    def input(key):
        game_manager.input(key)


    sky = Sky()
    app.run()

