import cv2 as cv
import time

from multiprocessing import Queue, Event

from config.logger import get_game_logger
from data_manager import DataManager
logger = get_game_logger()

class EmotionHolder():
    def __init__(self):
        self.dominant_emotion = None
        self.second_dominant_emotion = None

class CameraReader:
    def __init__(self, data_manager: DataManager):
        self.last_analysis_time = time.time()
        self.analysis_interval = 1
        self.emotion_holder = EmotionHolder()
        self.game_is_running = False
        self.data_manager = data_manager

    def run(self, queue: Queue, camera_ready_event: Event):
        from deepface.DeepFace import analyze # Importuję tutaj, żeby nie było problemów z importem w innych plikach (konkretnie blokuje wtedy workerów)

        cap = cv.VideoCapture(0)
        logger.info(f'Camera connected')
        while True:
            ret, frame = cap.read()
            # cv.imshow('Kamera', frame)
            if cap.isOpened():
                camera_ready_event.set()
            else:
                logger.error('Failed to connect to the camera')
                return
            if not queue.empty():
                logger.info(f'Processing queue for camera')
                self.game_is_running = queue.get()
            if time.time() - self.last_analysis_time > self.analysis_interval and self.game_is_running:
                try:
                    logger.info(f'Analyzing emotions...')
                    result = analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')[0]
                    logger.info(f'Result of analyzing emotions {result}')
                    self.emotion_holder.dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                    self.emotion_holder.second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]
                    logger.info(
                        f'Prevailing emotions: {self.emotion_holder.dominant_emotion} i {self.emotion_holder.second_dominant_emotion}')
                    self.data_manager.add_emotion(self.emotion_holder.dominant_emotion, self.emotion_holder.second_dominant_emotion)
                    logger.info(f'Added emotions to data manager')
                except Exception as e:
                    logger.error(f'Błąd podczas analizy: {e}')
                self.last_analysis_time = time.time()
                
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    camera_reading = CameraReader(DataManager())
    camera_reading.run()