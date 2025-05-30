import threading
import time
import multiprocessing
import tkinter as tk

FEEDBACK_PATH = r"feedback_folder"
SCREENSHOTS_PATH = r"screenshots_folder"

Harassment_Detected=multiprocessing.Event()
Harassment_Detected.is_set=False

frame_skip=5

global DEBUG
DEBUG = False

