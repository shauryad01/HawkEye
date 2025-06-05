import cv2
import numpy as np
import threading
import time
import settings
from keras.models import load_model
from queue import Queue
from HawkEyeApp import EventDetected
from utils import save_screenshot

# Load the classification model
try:
    model = load_model(settings.MODEL_PATH, compile=False)
except Exception as e:
    raise RuntimeError(f"[ERROR] Could not load model: {e}")

# Load class labels
try:
    with open(settings.LABELS_PATH, "r") as f:
        class_names = [line.strip() for line in f.readlines()]
except Exception as e:
    print(f"[WARN] Could not load labels: {e}")
    # Fallback labels
    class_names = ["Harassment", "NoHarassment"]

latest_confidence = 0.0

def run_detection(self,controller, frame_queue, event=settings.Harassment_Detected, ui_callback=None):
    print("[DETECT] Detection process started.")
    global latest_confidence
    frame_count = 0

    while not event.is_set:
        if frame_queue.empty():
            time.sleep(0.01)
            continue

        frame = frame_queue.get()

        # Validate frame
        if frame is None or not hasattr(frame, 'shape') or frame.size == 0:
            print("[WARN] Invalid frame received. Skipping.")
            continue

        # Rotate landscape frames
        h, w = frame.shape[:2]
        if w > h:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_count += 1
        if frame_count % settings.frame_skip != 0:
            continue

        try:
            # Preprocess the frame
            resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
            image = np.asarray(resized, dtype=np.float32).reshape(1, 224, 224, 3)
            image = image / 255.0  # Match training normalization

            # Prediction
            prediction = model.predict(image, verbose=0)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence = prediction[0][index]
            latest_confidence = confidence
            if ui_callback:
                ui_callback(f"{class_name} ({confidence * 100:.2f}%)")


            print(f"[DETECT] Class: {class_name} | Confidence: {confidence * 100:.2f}%")

            if settings.DEBUG:
                print("[DEBUG] Raw prediction vector:", prediction)
                for i, label in enumerate(class_names):
                    print(f"[DEBUG] {label}: {prediction[0][i]:.4f}")

            # Trigger on positive class with confidence
            if "True" in class_name and confidence >= settings.detection_threshold:
                print("[ALERT] Emergency Detected! Saving screenshot.")
                save_screenshot(frame, settings.SCREENSHOTS_PATH)
                event.set()
                EventDetected(self, controller)
                event.clear()

        except Exception as e:
            print(f"[ERROR] Detection failed: {e}")
            continue

    print("[DETECT] Detection process ended.")
