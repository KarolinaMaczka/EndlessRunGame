from states.state import GameState

from ursina import destroy, color, WindowPanel, Button, Text, Func, Entity
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from config.logger import get_game_logger

logger = get_game_logger()

class LevelSelect(GameState):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.create_window()

    def input(self, key):
        pass

    def update(self):
        pass

    def on_exit(self):
        super().on_exit()
        logger.info(f'Exiting settings')
        destroy(self.window_panel)

    def start(self):
        pass

    def create_window(self):
        menu = Entity()
        self.menu = DropdownMenu(
            text="Choose level",
            buttons=[DropdownMenuButton(f"Level {i}", on_click=Func(self.pass_level, i)) for i in
                     range(1, 4)],
            position=(-4, 0.25),
            scale=(8, 0.8),
            parent=menu,
            color=color.gray
        )
        self.window_panel = WindowPanel(
            title='Game Settings',
            content=(
                Button('Go back', color=color.red,
                       on_click=self.main_menu),
                menu
            ),
            position=(0, 0.25),
        )

    def pass_level(self, level_number):
        logger.info(f'Level {level_number} selected')
        temp_text = Text(
            text="Selected level " + str(level_number),
            position=(0, 0.4),
            origin=(0, 0),
            color=color.black
        )
        destroy(temp_text, delay=1.5)
        self.context.selected_level = level_number

    def main_menu(self):
        self.context.transition_to('main_menu')
    

