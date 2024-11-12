import cv2 as cv
import time

from multiprocessing import Queue, Value, Manager

from config.logger import get_game_logger
from data_manager import DataManager

logger = get_game_logger()

class EmotionHolder():
    def __init__(self):
        self.dominant_emotion = None
        self.second_dominant_emotion = None

class CameraReader:
    def __init__(self, data_manager: DataManager, list_manager: Manager):
        self.last_analysis_time = time.time()
        self.analysis_interval = 1
        self.emotion_holder = EmotionHolder()
        self.game_is_running = False
        self.data_manager = data_manager
        self.debug = False
        self.camera_index = Value('i', 0)
        self.cameras = list_manager.list()
        self.cameras = self.list_cameras()

    def run(self, queue: Queue):
        from deepface.DeepFace import analyze # Importuję tutaj, żeby nie było problemów z importem w innych plikach (konkretnie blokuje wtedy workerów)

        if self.cameras is not None and len(self.cameras) > 0:
            self.camera_index = self.cameras[0]
        cap = cv.VideoCapture(self.camera_index)
        logger.info(f'Camera connected')
        
        while True:
            if self.camera_index != cap.get(cv.CAP_PROP_INDEX):
                cap.release()
                cap = cv.VideoCapture(self.camera_index)
                logger.info(f'Camera changed to {self.camera_index}')
            try:
                ret, frame = cap.read()
            except Exception as e:
                logger.error(f'Błąd podczas odczytu kamery: {e}')
                break
            if not queue.empty():
                self.game_is_running = queue.get()
            if time.time() - self.last_analysis_time > self.analysis_interval and self.game_is_running:
                try:
                    logger.info(f'Analyzing emotions...')
                    result = analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')[0]
                    self.emotion_holder.dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                    self.emotion_holder.second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]

                    self.data_manager.add_emotion(self.emotion_holder.dominant_emotion, self.emotion_holder.second_dominant_emotion)
                    if self.debug:
                        logger.info(f'Analyzing emotions...')
                        logger.info(f'Result of analyzing emotions {result}')
                        logger.info(f'Prevailing emotions: {self.emotion_holder.dominant_emotion} i {self.emotion_holder.second_dominant_emotion}')
                except Exception as e:
                    logger.error(f'Błąd podczas analizy: {e}')
                self.last_analysis_time = time.time()
                
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
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
        return self.cameras

    def change_camera(self, camera_number):
        logger.info(f'Camera {camera_number} clicked')
        self.camera_index = camera_number

if __name__ == '__main__':
    camera_reading = CameraReader(DataManager(), Manager())
    camera_reading.run()