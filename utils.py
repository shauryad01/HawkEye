import os
import time, datetime
import cv2
import subprocess
import settings
import threading
import model_training
import HawkEyeApp



def save_screenshot(frame, folder):
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


def open_detection_screen(self, video_source):
    self.controller.show_frame("DetectionScreen")
    detection_frame = self.controller.frames["DetectionScreen"]
    if settings.DEBUG:
        threading.Thread(target=lambda: HawkEyeApp.DetectionScreen.start_camera(video_source=1, self=detection_frame), daemon=True).start()
    else:
        threading.Thread(target=lambda: HawkEyeApp.DetectionScreen.start_camera(video_source=0, self=detection_frame), daemon=True).start()


def start_detection_pipeline(self,video_source, frame_queue, event, ui_callback=None):
    event.is_set = False
    if not self.running:
        self.start_camera(video_source)
    from detection_module import run_detection
    threading.Thread(target=run_detection,args=(self, self.controller, frame_queue, event, ui_callback), daemon=True).start()

def start_model_training(root):
    from HawkEyeApp import training_progress

    loading_window = training_progress(root)

    def retrain_and_close():
        model_training.retrain_model()
        root.after(0, loading_window.destroy)

    threading.Thread(target=retrain_and_close, daemon=True).start()