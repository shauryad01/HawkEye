import cv2
import threading

global emergency_triggered
emergency_triggered = None
emergency_triggered = threading.Event()

DEBUG = False    # Uses microphone
DEBUG1 = False   # Does not use microphone

MIC_SENSITIVITY_THRESHOLD = 75
MIC_TIMEOUT = 10
MIC_PHRASE_TIME_LIMIT = 10

emergency_words = {"help", "stop"}


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")