import cv2 as cv
import numpy as np

def read_camera():
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    read_camera()