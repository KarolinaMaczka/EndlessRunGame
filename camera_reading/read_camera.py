import cv2 as cv
import time
from deepface import DeepFace

class EmotionHolder():
    def __init__(self):
        self.dominant_emotion = None
        self.second_dominant_emotion = None

class CameraReader:
    def __init__(self):
        self.last_analysis_time = time.time()
        self.analysis_interval = 5
        self.emotion_holder = EmotionHolder()
        self.game_is_running = False
    def run(self):
        cap = cv.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            # cv.imshow('Kamera', frame)

            if time.time() - self.last_analysis_time > self.analysis_interval and self.game_is_running:
                try:
                    print('Analizuję...')
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')[0]
                    self.emotion_holder.dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                    self.emotion_holder.second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]
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
    camera_reading = CameraReader()
    camera_reading.run()