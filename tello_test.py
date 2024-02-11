from djitellopy import Tello
import cv2
import threading
import time
import numpy as np

def perform_flip():
    while True:
        print(tel.get_battery())
        time.sleep(5)

tel = Tello()

tel.connect()

tel.takeoff()

tel.streamon()

kernel = np.ones((2, 2), np.uint8)
faces = cv2.CascadeClassifier('faces.xml')

cv2.namedWindow("Tello Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Tello Video", 960, 720)

flip_thread = threading.Thread(target=perform_flip)
flip_thread.start()

while True:
    frame = tel.get_frame_read().frame

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rezults = faces.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4)
    
    for (x, y, w, h) in rezults:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
    cv2.imshow("ok", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
    elif key == ord('a'):
        tel.move_left(10)
    elif key == ord('d'):
        tel.move_right(10)
    elif key == ord('w'):
        tel.move_up(10)
    elif key == ord('s'):
        tel.move_down(10)
    cv2.imshow("Tello Video", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

tel.streamoff()

tel.land()

cv2.destroyAllWindows()

flip_thread.join()




