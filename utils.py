import os
import time, datetime
import cv2
import subprocess
import settings
import threading
import HawkEyeApp


def save_screenshot(frame, folder=settings.SCREENSHOTS_PATH):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"screenshot_{timestamp}.jpg")

    # Save the frame as an image
    cv2.imwrite(filename, frame)
    print(f"[SCREENSHOT] Saved to {filename}")


def open_feedback_folder(self):
        folder_path = os.path.abspath(settings.FEEDBACK_PATH)
        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(folder_path, "false_positive"), exist_ok=True)
        os.makedirs(os.path.join(folder_path, "false_negative"), exist_ok=True)
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == "nt" else ["open", folder_path])

def open_screenshots_folder(self):
    folder_path = os.path.abspath(settings.SCREENSHOTS_PATH)
    os.makedirs(folder_path, exist_ok=True)
    subprocess.Popen(f'explorer "{folder_path}"' if os.name == "nt" else ["open", folder_path])


def open_detection_screen(self):
    self.controller.show_frame("DetectionScreen")
    detection_frame = self.controller.frames["DetectionScreen"]
    threading.Thread(target=lambda: HawkEyeApp.DetectionScreen.start_camera(detection_frame), daemon=True).start()