import cv2 as cv
import time
from deepface import DeepFace

def read_camera():

    last_analysis_time = time.time()
    analysis_interval = 5

    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv.imshow('Kamera', frame)

        #Analiza emocji co 5 sekund
        if time.time() - last_analysis_time > analysis_interval:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')
                print(result)
            except Exception as e:
                print(f'Błąd podczas analizy: {e}')
            last_analysis_time = time.time()
            
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    
if __name__ == '__main__':
    read_camera()