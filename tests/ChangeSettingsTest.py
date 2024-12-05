import unittest
from unittest.mock import Mock
from multiprocessing import Value

from ursina import Ursina

from states.impl.change_settings import SettingsMenu

class test_ChangeSettings(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.context = Mock()
        self.context.camera_reader = Mock()
        self.context.camera_reader.cameras = [0, 1]
        self.context.camera_reader.is_in_settings.value = True

        ursina = Ursina()
    
    @classmethod
    def setUp(self):
        self.settings_menu = SettingsMenu(self.context)

    def test_passing_camera(self):
        print("Test passing camera")
        self.settings_menu.pass_camera(1)
        self.context.camera_reader.change_camera.assert_called_with(1)

        self.assertRaises(TypeError, self.settings_menu.pass_camera, '1')
        self.assertRaises(TypeError, self.settings_menu.pass_camera, None)
    
    def test_camera_buttons(self):
        print("Test camera buttons")
        self.settings_menu.create_window()
        self.assertEqual(len(self.settings_menu.menu.buttons), 2)
        buttons = self.settings_menu.menu.buttons
        for i in range(0,len(buttons)):
            buttons[i].on_click()
            # Zakładamy, że do procesu read_camera przesyłamy indeks kamery pomniejszony już o 1
            self.context.camera_reader.change_camera.assert_called_with(i)

    def test_no_cameras(self):
        print("Test no cameras")
        context = self.context
        context.camera_reader.cameras = []
        settings_menu = SettingsMenu(context)
        settings_menu.create_window()
        context.transition_to.assert_called_with('main_menu')
