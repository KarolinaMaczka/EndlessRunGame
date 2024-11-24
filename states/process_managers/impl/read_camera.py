import cv2 as cv
import time

from multiprocessing import Queue, Value, Manager, Event, Process

from config.logger import get_game_logger
from data_manager import DataManager
from states.process_managers.process_manager import ProcessManager

logger = get_game_logger()

class CameraReader(ProcessManager):
    def __init__(self, manager: Manager): # type: ignore
        super().__init__()
        self.last_analysis_time = time.time()
        self.analysis_interval = 1
        self.game_is_running = Value('b', False)
        self.debug = True
        self.current_camera_index = Value('i', 0)
        self.passed_camera_index = Value('i', 0)
        self.cameras = manager.list()
        self.is_in_settings = Event()
        self.emotion_queue = Queue()
        self.camera_ready_event = Event()
        self.list_cameras()
        self.process = Process(target=self.run, args=(self.game_is_running, self.emotion_queue, self.camera_ready_event))
        self.process.start()

    def run(self, game_is_running: Value, emotion_queue: Queue, camera_ready_event: Event):
        from deepface.DeepFace import analyze # Importuję tutaj, żeby nie było problemów z importem w innych plikach (konkretnie blokuje wtedy workerów)

        if self.cameras is not None and len(self.cameras) > 0:
            self.current_camera_index.value = self.cameras[0]
        cap = cv.VideoCapture(self.current_camera_index.value)
        logger.info(f'Camera connected')
        
        while True:
            # Check if camera has been changed
            if self.current_camera_index.value != self.passed_camera_index.value:
                logger.info(f'Changing camera from {self.current_camera_index.value} to {self.passed_camera_index.value}')
                cap.release()
                self.current_camera_index.value = self.passed_camera_index.value
                cap = cv.VideoCapture(self.current_camera_index.value)
                logger.info(f'Camera changed to {self.passed_camera_index.value}')
            try:
                ret, frame = cap.read()
            except Exception as e:
                logger.error(f'Failed to connect to the camera: {e}')
                break
            if self.is_in_settings.is_set():
                cv.imshow('Camera', frame)
            else:
                cv.destroyAllWindows()

            if cap.isOpened():
                camera_ready_event.set()
            else:
                camera_ready_event.set()
                logger.error('Failed to connect to the camera')
                return

            if time.time() - self.last_analysis_time > self.analysis_interval and game_is_running.value:
                try:
                    logger.info(f'Analyzing emotions...')
                    result = analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')[0]
                    dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                    second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]
                    dominant_emotion_value = result['emotion'][dominant_emotion]
                    second_dominant_emotion_value = result['emotion'][second_dominant_emotion]
                    emotions_and_values = ( (dominant_emotion, dominant_emotion_value),
                                            (second_dominant_emotion, second_dominant_emotion_value),
                                            result['face_confidence']
                                        )
                    # Put emotions to queue so that they can be read by the difficulty logic
                    emotion_queue.put(emotions_and_values)
                    if self.debug:
                        logger.info(f'Result of analyzing emotions {result}')
                        logger.info(f'Prevailing emotions: {dominant_emotion} i {second_dominant_emotion}')
                except Exception as e:
                    logger.error(f'Błąd podczas analizy: {e}')
                self.last_analysis_time = time.time()
            cv.waitKey(1)
        cap.release()
        cv.destroyAllWindows()

    def list_cameras(self):
        index = 0
        while True:
            cap = cv.VideoCapture(index)
            if not cap.read()[0]:
                break
            self.cameras.append(index)
            cap.release()
            index += 1
        logger.info(f'Found {len(self.cameras)} cameras')
        for i in self.cameras:
            logger.info(f'Camera {i}')
        return

    def change_camera(self, camera_number):
        logger.info(f'Camera {camera_number} clicked')
        self.passed_camera_index.value = camera_number

    def toggle_run(self):
        self.game_is_running.value = not self.game_is_running.value

    def on_exit(self):
        cv.destroyAllWindows()
        super().on_exit()
        logger.info(f'Deleted camera process')

if __name__ == '__main__':
    camera_reading = CameraReader(DataManager(), Manager())
    camera_reading.run()