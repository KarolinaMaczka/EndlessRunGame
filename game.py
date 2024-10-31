from ursina import *

from entities.camera import PlayerCamera
from game_manager import GameManager
from entities.player import Player
from scenery import Scenery
import atexit

import threading
from camera_reading.read_camera import read_camera


if __name__ == '__main__':

    app = Ursina()

    window.fps_counter.enabled = True
    #TODO fill
    window.title = 'Fill this'

    player = Player()

    camera = PlayerCamera(player)

    scenery = Scenery()

    game_manager = GameManager(player, camera)


    def update():
        game_manager.update()


    atexit.register(game_manager.on_exit)

    sky = Sky()

    # Add multithreading so that we can read camera in the background
    threading.Thread(target=read_camera, daemon=True).start()

    app.run()
