import cv2 as cv
from deepface import DeepFace
import time

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    last_time = time.time()
    while True:
        ret, frame = cap.read()
        
        current_time = time.time()
        if current_time - last_time >= 5:
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend="mtcnn")[0]
                dominant_emotion = max(result['emotion'], key=result['emotion'].get)
                second_dominant_emotion = sorted(result['emotion'], key=result['emotion'].get)[-2]
                dominant_emotion_value = result['emotion'][dominant_emotion]
                second_dominant_emotion_value = result['emotion'][second_dominant_emotion]
                print(f"Dominant emotion: {dominant_emotion}, value: {dominant_emotion_value}")
                print(f"Second dominant emotion: {second_dominant_emotion}, value: {second_dominant_emotion_value}")
                print(f"result: {result}")
                print("-------------------------------------", end="\n\n")


            except Exception as e:
                print(f"Error: {e}")
            last_time = current_time

        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()