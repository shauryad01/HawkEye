import threading
import time
import multiprocessing
import tkinter as tk

FEEDBACK_PATH = r"feedback_folder"
FEEDBACK_PATH_false_neg = r"feedback_folder\false_negative"
FEEDBACK_PATH_false_pos = r"feedback_folder\false_positive"
SCREENSHOTS_PATH = r"screenshots_folder"

MODEL_PATH= "mobilenetv2_with_feedback.h5"
LABELS_PATH= "labels.txt"


global Harassment_Detected
Harassment_Detected=threading.Event()
Harassment_Detected.clear()

detection_threshold = 0.85

frame_skip=1

global DEBUG
DEBUG = False

