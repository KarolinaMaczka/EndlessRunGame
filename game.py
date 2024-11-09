from ursina import *

from entities.camera import PlayerCamera
from game_manager import GameManager
from entities.player import Player
from scenery import Scenery
import atexit


from multiprocessing import Process, Queue, Manager
from camera_reading.read_camera import CameraReader
from data_manager import DataManager


if __name__ == '__main__':

    list_manager = Manager()
    data_manager = DataManager(list_manager)

    queue = Queue()
    camera_reading = CameraReader(data_manager)
    p = Process(target=camera_reading.run, args=(queue,))
    p.start()

    def on_exit():
        p.terminate()
        p.join()
        
    atexit.register(on_exit)

    app = Ursina()

    window.fps_counter.enabled = True
    #TODO fill
    window.title = 'Fill this'

    player = Player()

    camera = PlayerCamera(player)

    scenery = Scenery()

    game_manager = GameManager(player, camera, data_manager, queue, camera_reading)

    def update():
        game_manager.update()

    atexit.register(game_manager.on_exit)

    sky = Sky()

    app.run()
