import tkinter as tk
from tkinter import ttk
import cv2
import time
import settings 
from utils import *
import threading
import queue
frame_queue = queue.Queue(maxsize=10)

class HawkEyeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HawkEye Security System")
        self.geometry("1000x700")
        self.protocol("WM_DELETE_WINDOW", self.quit)

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frames = {}

        for F in (MainMenu, DetectionScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Hawkeye Security System", font=('Arial', 24)).pack(pady=(20, 30))

        tk.Button(frame, text="Start Detection", font=('Arial', 16), width=25, command=lambda: open_detection_screen(self)).pack(pady=15)

        tk.Button(frame, text="Open Feedback Folder", font=('Arial', 16), width=25, command=lambda:open_feedback_folder(self)).pack(pady=15)

        tk.Button(frame, text="Open Screenshots Folder", font=('Arial', 16), width=25, command=lambda:open_screenshots_folder(self)).pack(pady=15)

        tk.Button(frame, text="Retrain Detection Model", font=('Arial', 16), width=25, command=lambda: start_model_training(self)).pack(pady=15)

        tk.Button(frame, text="Quit", font=('Arial', 16), width=25, command=quit).pack(pady=15)

class training_progress(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Training Model")
        self.geometry("400x150")
        self.resizable(False, False)

        tk.Label(self, text="Training model...\nPlease wait", font=("Arial", 14)).pack(pady=20)
        self.progress = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.progress.pack(pady=10)
        self.progress.start()

class DetectionScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cap = None
        self.running = False

        tk.Label(self, text="Detection Module", font=("Arial", 20)).pack(pady=20)

        self.video_label = tk.Label(self)
        self.video_label.pack(pady=10)
        
        self.cap = None
        self.running = False

        tk.Button(self, text="Run Detection", font=("Arial", 16), command=lambda: start_detection_pipeline(self, target="run_detection", frame_queue=frame_queue, event = settings.Harassment_Detected, ui_callback=self.update_detection_label)).pack(pady=15)
        self.detection_label = tk.Label(self, text="", font=("Arial", 16))
        self.detection_label.place(relx=1, rely=0, x=-30, y=25, anchor="ne")
        

        if settings.DEBUG:
            from HawkEyeApp import EventDetected
            tk.Button(self, text="DEBUGGING: MANUAL EVENT SET", font=("Arial", 16), command=lambda: EventDetected(self, controller=self.controller)).place(relx=0, rely=0, x=150, y=250)
        tk.Button(self, text="← Back to Menu", font=("Arial", 16), command=self.back_to_menu).place(relx=0, rely=0, x=1, y=15)

    def update_detection_label(self, text):
        if "Harassment" in text:
            color = "red"
        if "NoHarassment" in text:
            color = "green"
        self.detection_label.config(text=f"Detection: {text}", fg=color)

    
    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            time.sleep(1)
            self.running = True
            self.show_cam()
        
    def show_cam(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                import cv2
                from PIL import Image, ImageTk
                try:
                    frame_queue.put_nowait(frame.copy())
                except queue.Full:
                    pass

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
            self.after(30, self.show_cam)
        else:
            self.video_label.config(image='')

    def back_to_menu(self):
        if self.running:
            self.running = False
            if self.cap:
                self.cap.release()
            self.video_label.config(image='')
        self.controller.show_frame("MainMenu")


class EventDetected(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title("HARASSMENT DETECTED ‼️")
        self.geometry("380x200")
        self.configure(bg="red")

        label = tk.Label(self, text="⚠️ Harassment Event Detected!", font=("Arial", 14), bg="red", fg="white")
        label.pack(pady=10)

        # Create a frame to hold the buttons
        btn_frame = tk.Frame(self, bg="red")
        btn_frame.pack(pady=20)

        # False Positive Button
        btn_fp = tk.Button(btn_frame, text="False Positive", font=("Arial", 12),command=lambda: self.fp_btn(folder=settings.FEEDBACK_PATH_false_pos))
        btn_fp.pack(side="left", padx=10)

        # OK Button
        btn_ok = tk.Button(btn_frame, text="OK", font=("Arial", 12),command=lambda: self.ok_btn(folder=settings.SCREENSHOTS_PATH))
        btn_ok.pack(side="left", padx=10)

        # False Negative Button
        btn_fn = tk.Button(btn_frame, text="False Negative", font=("Arial", 12),command=lambda: self.fn_btn(folder=settings.FEEDBACK_PATH_false_neg))
        btn_fn.pack(side="left", padx=10)


    def fp_btn(self, folder):
        if not frame_queue.empty():
            frame = frame_queue.get()
            save_screenshot(frame, folder)
        self.destroy()

    def fn_btn(self, folder):
        if not frame_queue.empty():
            frame = frame_queue.get()
            save_screenshot(frame, folder)
        self.destroy()

    def ok_btn(self, folder):
        if not frame_queue.empty():
            frame = frame_queue.get()
            save_screenshot(frame, folder)
        self.destroy()



