from camera_reading.read_camera import EmotionHolder

class DifficultyLogic():
    def __init__(self):
        self.emotion_holder = EmotionHolder()
        self.difficulty_level = 1
        self.difficulty_level_max = 2
        self.difficulty_level_min = 1