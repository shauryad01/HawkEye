import cv2
import time
import settings
import numpy as np

def cam_active(event):
    
    if not event.is_set():
        cap = cv2.VideoCapture(0)
        time.sleep(1)  # Camera warm-up time

        while cap.isOpened():
            _, frame = cap.read()
            if not _:
                break
            
            cv2.imshow("Camera", frame)

            if event.is_set():
                print("[CAM] Emergency detected! Stopping camera.")
                break

            if cv2.waitKey(1) == ord('q'):  
                event.set()
                break

    cap.release()
    cv2.destroyAllWindows()
    print("[CAM] Camera process stopped.")


