from ursina import *

from entities.camera import PlayerCamera
from game_manager import GameManager
from entities.player import Player
from scenery import Scenery

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


sky = Sky()

app.run()
