from ursina import destroy, color, WindowPanel, Button, application, Func, Entity, Text

from states.state import GameState
from config.logger import get_game_logger

logger = get_game_logger()

class GameOver(GameState):
    def __init__(self, context):
        super().__init__()
        self.rating = -1
        self.context = context
        self.score = self.context.player.Z
        logger.info(f'game over, score: {self.score}')
        self.context.data_manager.add_score(self.score)
        self.create_window()

    def input(self, key):
        pass

    def update(self):
        pass

    def on_exit(self):
        super().on_exit()
        logger.info(f'Exiting game over state')
        self.context.data_manager.save()
        self.context.data_manager.clean_data()
        destroy(self.window_panel)

    def start(self):
        self.context.transition_to('running_state')

    def main_menu(self):
        self.context.transition_to('main_menu')

    def create_window(self):
        self.window_panel = WindowPanel(
            title='Game Over :(',
            content=(
                Text(f'Your score: {self.score}', color=color.gray),
                Text('I am satisfied: ', color=color.gray),
                self.create_star_buttons('satisfaction'),
                Text('I felt challenged: ', color=color.gray),
                self.create_star_buttons('challenge'),
                Text('I felt bored: ', color=color.gray),
                self.create_star_buttons('boredom'),
                Button('Try Again', color=color.gray, on_click=self.start),
                Button('Main Menu', color=color.gray, on_click=self.main_menu),
                Button('Quit', color=color.red, on_click=application.quit)
            ),
            position=(0, 0.4)
        )

    def create_star_buttons(self, typ='satisfaction'):
        star_container = Entity()
        stars = []
        # self.stars = []
        rating = 0

        for i in range(5):
            star = Button(
                # model='quad',
                text='+',
                color=color.clear,
                highlight_color=color.clear,
                pressed_color=color.clear,
                scale=(1, 1),
                position=(-2 + i, 0, 0),
                parent=star_container,
                on_click=Func(self.set_rating, typ, i + 1)
            )
            star.text_entity.color = color.yellow if i < getattr(self, f'rating_{typ}', 0) else color.gray
            stars.append(star)
        setattr(self, f'stars_{typ}', stars)

        return star_container

    def set_rating(self, typ, rating):
        logger.info(f'Setting satisfaction rating to {rating}')
        setattr(self, f'rating_{typ}', rating)
        method = getattr(self.context.data_manager, f"add_player_{typ}", None)
        if callable(method):
            method(rating)
        for i, star in enumerate(getattr(self, f'stars_{typ}', [])):
            star.text_entity.color = color.yellow if i < rating else color.gray

