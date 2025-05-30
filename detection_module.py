import cv2
import numpy as np
from keras.models import load_model
import queue
import settings
import threading
import time
from utils import save_screenshot

# Load the model and class labels once
model = load_model("efficientnetb0_classifier.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

import os
import datetime

latest_confidence = 0.0

def run_detection(self, frame_queue, event):
    print("[DETECT] Detection process started.")
    global latest_confidence
    frame_skip = settings.frame_skip
    frame_count = 0
    settings.detection_threshold = 0.85  # Optional, for future use

    while not event.is_set():
        if not frame_queue.empty():
            frame = frame_queue.get()
            # confidence = gui.fake_model_confidence(frame)
            # latest_confidence = confidence
            # Validate the frame before using it
            if frame is None or not hasattr(frame, 'shape') or frame.size == 0:
                print("[DETECT] Invalid frame received. Skipping.")
                continue
                
            try:
                # Rotate frame if it's in landscape orientation
                h, w = frame.shape[:2]
                if w > h:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

                try:
                    display_frame = frame.copy()
                except Exception as e:
                    print(f"[DETECT] Failed to copy frame: {e}")
                    continue

            except Exception as e:
                print(f"[DETECT] Failed to copy frame: {e}")
                continue

            frame_count += 1

            if frame_count % frame_skip == 0:
                try:
                    resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
                    image = np.asarray(resized, dtype=np.float32).reshape(1, 224, 224, 3)
                    image = (image / 127.5) - 1

                    prediction = model.predict(image, verbose=0)
                    index = np.argmax(prediction)
                    class_name = class_names[index].strip()
                    confidence_score = prediction[0][index]

                    print(f"[DETECT] Class: {class_name} | Confidence: {confidence_score*100:.2f}%")

                    if class_name == "0 Harassment True" and confidence_score >= 0.85:
                        print("[DETECT] Emergency Detected!")
                        save_screenshot(frame)
                        event.set()
                    
                except Exception as e:
                    print(f"[DETECT] Prediction failed: {e}")
                    continue
