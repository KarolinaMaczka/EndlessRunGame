import unittest
from unittest.mock import Mock
from multiprocessing import Value

from ursina import Ursina

from states.impl.level_select import LevelSelect

class test_ChangeSettings(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.context = Mock()
        self.context.level_names = {
        3: "Training/Chill",
        6: "Balanced",
        9: "Challenging"
    }
    
        ursina = Ursina()
    
    @classmethod
    def setUp(self):
        self.context.possible_levels = [3,6,9]
        self.context.selected_level = self.context.possible_levels[0]  # Set to a valid key from self.context.level_names
        self.level_selection = LevelSelect(self.context)


    def test_passing_level(self):
        print("Test passing selected level")
        self.level_selection.pass_level(6)
        self.assertEqual(self.context.selected_level, 6)

        self.assertRaises(TypeError, self.level_selection.pass_level, '6')
        self.assertRaises(TypeError, self.level_selection.pass_level, None)
    
    def test_level_buttons(self):
        print("Test level buttons")
        self.level_selection.create_window()
        self.assertEqual(len(self.level_selection.menu.buttons), len(self.context.possible_levels))
        buttons = self.level_selection.menu.buttons
        for i in range(0,len(buttons)):
            buttons[i].on_click()
            self.assertEqual(self.context.selected_level, self.context.possible_levels[i])

