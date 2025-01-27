from ursina import destroy, color, WindowPanel, Button, Func, Entity
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton, Text
from states.process_managers.impl.read_camera import CameraReader

from config.logger import get_game_logger
from states.state import GameState

logger = get_game_logger()


class SettingsMenu(GameState):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.create_window()
        self.context.camera_reader.is_in_settings.value = True

    def input(self, key):
        pass

    def update(self):
        pass

    def start(self):
        pass

    def on_exit(self):
        super().on_exit()
        logger.info(f'Exiting settings')
        destroy(self.window_panel)
        self.context.camera_reader.is_in_settings.value = False

    def main_menu(self):
        self.context.transition_to('main_menu')

    def pass_camera(self, camera_number):
        if not isinstance(camera_number, int):
            raise TypeError('Camera number must be an integer')
        self.context.camera_reader.change_camera(camera_number)

        logger.info(f'Settings: Camera {camera_number} selected')
        temp_text = Text(
        text="Selected Camera " + str(camera_number),
        position=(0, 0.4),
        origin=(0, 0),
        color=color.black
        )
        destroy(temp_text, delay=1.5)

    def create_window(self):
        camera_count = len(self.context.camera_reader.cameras)
        if camera_count == 0:
            logger.error('Settings - No cameras to show, back to main menu')
            temp_text = Text(
            text="No cameras found",
            position=(0, 0.4),
            origin=(0, 0),
            color=color.black
            )
            destroy(temp_text, delay=1.5)
            self.main_menu()
            return
        
        menu = Entity()
        self.menu = DropdownMenu(
            text="Choose a camera",
            buttons=[DropdownMenuButton(f"Camera {i}", on_click=Func(self.pass_camera, i - 1)) for i in
                     range(1, camera_count + 1)],
            position=(-4, 0.25),
            scale=(8, 0.8),
            parent=menu,
            color=color.gray
        )
        self.window_panel = WindowPanel(
            title='Settings',
            content=(
                Button('Go back', color=color.red,
                       on_click=self.main_menu),
                menu
            ),
            position=(0, 0.25),
        )

