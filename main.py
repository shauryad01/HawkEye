import cv2
import time
import datetime
from micActive import get_volume

mic=True
FaceCam=True

face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
body_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_fullbody.xml")
# hand_cascade = cv2.CascadeClassifier("C:\Projects\HawkEye\HawkEye\hand.xml")



if mic or FaceCam:
        cap=cv2.VideoCapture(0)
        while True:            
            _, frame=cap.read()
            cv2.imshow('Camera', frame)
            
            # vol=next(get_volume())
            
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
            # hands = hand_cascade.detectMultiScale(gray, 1.3, 5)   
                
            # if vol>=75:    
            for(x, y, width, height) in faces:
                cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
                            
            for(x, y, width, height) in bodies:
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 3)
                                
                # for(x, y, width, height) in hands:
                #     cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)
            if cv2.waitKey(1)==ord('q'):
                break
cap.release()
cv2.destroyAllWindows()