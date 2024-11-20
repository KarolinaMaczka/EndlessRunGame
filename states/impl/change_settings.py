from ursina import destroy, color, WindowPanel, Button, Func, Entity
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from states.process_managers.impl.read_camera import CameraReader

from config.logger import get_game_logger
from states.state import GameState

logger = get_game_logger()


class SettingsMenu(GameState):
    def __init__(self, context, camera_reader: CameraReader):
        super().__init__()
        self.context = context
        self.create_window(len(camera_reader.cameras))
        self.camera_reader = camera_reader
        self.camera_reader.is_in_settings.set()

    def input(self, key):
        pass

    def update(self):
        pass

    def start(self):
        pass

    def on_exit(self):
        super().on_exit()
        logger.info(f'Exiting settings')
        destroy(self.context.window_panel)
        self.context.window_panel = None
        self.camera_reader.is_in_settings.clear()

    def main_menu(self):
        self.context.transition_to('main_menu')

    def pass_camera(self, camera_number):
        print(f'Camera {camera_number} clicked')
        self.context.camera_reader.change_camera(camera_number - 1)

    def create_window(self, camera_count):
        menu = Entity()
        self.context.menu = DropdownMenu(
            text="Choose a camera",
            buttons=[DropdownMenuButton(f"Camera {i}", on_click=Func(self.pass_camera, i)) for i in
                     range(1, camera_count + 1)],
            position=(-4, 0.25),
            scale=(8, 0.8),
            parent=menu,
            color=color.gray
        )
        self.context.window_panel = WindowPanel(
            title='Settings',
            content=(
                Button('Go back', color=color.red,
                       on_click=self.main_menu),
                menu
            ),
            position=(0, 0.25),
        )

