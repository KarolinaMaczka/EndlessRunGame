from ursina import destroy, color, WindowPanel, Button, application, Func, Entity, Text

from states.state import GameState


class GameOver(GameState):
    def __init__(self, context):
        self.rating = -1
        self.context = context
        self.create_window()

    def handle_input(self):
        pass

    def update(self):
        pass

    def on_exit(self):
        self.context.data_manager.save()
        self.context.data_manager.clean_data()
        destroy(self.context.window_panel)
        self.context.window_panel = None

    def start(self):
        self.context.transition_to('running_state')

    def main_menu(self):
        self.context.transition_to('main_menu')

    def create_window(self):
        self.context.window_panel = WindowPanel(
            title='Game Over :(',
            content=(
                Text('Rate your gameplay satisfaction: ', color=color.gray),
                self.create_star_buttons(),
                Button('Try Again', color=color.gray, on_click=self.start),
                Button('Main Menu', color=color.gray, on_click=self.main_menu),
                Button('Quit', color=color.red, on_click=application.quit)
            ),
            position=(0, 0.25)
        )

    def create_star_buttons(self):
        star_container = Entity()
        self.stars = []
        self.rating = 0

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
                on_click=Func(self.set_rating, i + 1)
            )
            star.text_entity.color = color.yellow if i < self.rating else color.gray
            self.stars.append(star)

        return star_container

    def set_rating(self, rating):
        self.rating = rating
        self.context.data_manager.save_player_satisfaction(rating)
        for i, star in enumerate(self.stars):
            star.text_entity.color = color.yellow if i < rating else color.gray

