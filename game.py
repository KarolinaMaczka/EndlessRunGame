from ursina import *

from entities.camera import PlayerCamera
from game_manager import GameManager
from entities.player import Player
from scenery import Scenery
import atexit

import threading
from camera_reading.read_camera import CameraReader
from data_manager import DataManager

if __name__ == '__main__':


    app = Ursina()

    window.fps_counter.enabled = True
    #TODO fill
    window.title = 'Fill this'

    player = Player()

    camera = PlayerCamera(player)

    data_manager = DataManager()

    camera_reading = CameraReader(data_manager)

    scenery = Scenery()

    game_manager = GameManager(player, camera, camera_reading, data_manager)

    threading.Thread(target=camera_reading.run, daemon=True).start()

    def update():
        game_manager.update()

    atexit.register(game_manager.on_exit)

    sky = Sky()

    #TODO Change to new process instead of thread

    app.run()
