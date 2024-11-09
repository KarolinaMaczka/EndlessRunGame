import cv2 as cv
import time

from multiprocessing import Queue

from data_manager import DataManager

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
        self.debug = False

    def run(self, queue: Queue):
        from deepface.DeepFace import analyze # Importuję tutaj, żeby nie było problemów z importem w innych plikach (konkretnie blokuje wtedy workerów)

        cap = cv.VideoCapture(0)
        print('camera connected')
        while True:
            ret, frame = cap.read()
            # cv.imshow('Kamera', frame)
            if not queue.empty():
                self.game_is_running = queue.get()
            if time.time() - self.last_analysis_time > self.analysis_interval and self.game_is_running:
                try:
                    print('Analizuję...')
                    result = analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')[0]
                    self.emotion_holder.dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                    self.emotion_holder.second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]

                    self.data_manager.add_emotion(self.emotion_holder.dominant_emotion, self.emotion_holder.second_dominant_emotion)
                    if self.debug:
                        print(f'Dominujące emocje: {self.emotion_holder.dominant_emotion} i {self.emotion_holder.second_dominant_emotion}')
                        print(result)
                except Exception as e:
                    print(f'Błąd podczas analizy: {e}')
                self.last_analysis_time = time.time()
                
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    camera_reading = CameraReader(DataManager())
    camera_reading.run()