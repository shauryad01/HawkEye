import settings
import subprocess
import os

def open_feedback_folder():
        folder_path = os.path.abspath(settings.FEEDBACK_PATH)
        os.makedirs(folder_path, exist_ok=True)
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == "nt" else ["open", folder_path])

def open_screenshots_folder():
        folder_path = os.path.abspath(settings.SCREENSHOTS_PATH)
        os.makedirs(folder_path, exist_ok=True)
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == "nt" else ["open", folder_path])