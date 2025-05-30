import tkinter as tk
from detection_module import run_detection
from detection_module import start_camera
from model_training import retrain_model
import cv2
import subprocess
import settings 
import os

def open_detection_screen(self):
    self.controller.show_frame("DetectionScreen")
    detection_frame = self.controller.frames["DetectionScreen"]
    start_camera(detection_frame)

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

        tk.Button(frame, text="Open Feedback Folder", font=('Arial', 16), width=25, command=self.open_feedback_folder).pack(pady=15)

        tk.Button(frame, text="Open Screenshots Folder", font=('Arial', 16), width=25, command=self.open_screenshots_folder).pack(pady=15)

        tk.Button(frame, text="Retrain Detection Model", font=('Arial', 16), width=25, command=retrain_model).pack(pady=15)

        tk.Button(frame, text="Quit", font=('Arial', 16), width=25, command=quit).pack(pady=15)

    def open_feedback_folder(self):
        folder_path = os.path.abspath(settings.FEEDBACK_PATH)
        os.makedirs(folder_path, exist_ok=True)
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == "nt" else ["open", folder_path])

    def open_screenshots_folder(self):
        folder_path = os.path.abspath(settings.SCREENSHOTS_PATH)
        os.makedirs(folder_path, exist_ok=True)
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == "nt" else ["open", folder_path])

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

        tk.Button(self, text="Run Detection", font=("Arial", 16), command=run_detection).pack(pady=15)

        self.detection_label = tk.Label(self, text="Detection: 0%", font=("Arial", 16))
        self.detection_label.place(relx=1, rely=0, x=-30, y=25, anchor="ne")


        tk.Button(self, text="← Back to Menu", font=("Arial", 16), command=self.back_to_menu).place(relx=0, rely=0, x=1, y=15)

    
    def show_cam(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                import cv2
                from PIL import Image, ImageTk

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


# class MainMenu(tk.Frame):
    
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller

#         frame = tk.Frame(self)
        
#         frame.pack(expand=True, fill="both")
        
#         tk.Label(frame, text="Hawkeye Security System", font=('Arial', 24)).pack(pady=(20, 30))

#         tk.Button(frame, text="Start Detection", font=('Arial', 16), width=25, command=lambda: open_detection_screen(self)).pack(pady=15)

#         tk.Button(frame, text="Open Feedback Folder", font=('Arial', 16), width=25, command=open_feedback_folder).pack(pady=15)

#         tk.Button(frame, text="Open Screenshots Folder", font=('Arial', 16), width=25, command=open_screenshots_folder).pack(pady=15)

#         tk.Button(frame, text="Retrain Detection Model", font=('Arial', 16), width=25, command=retrain_model).pack(pady=15)

#         tk.Button(frame, text="Quit", font=('Arial', 16), width=25, command=quit).pack(pady=15)

if __name__ == "__main__":
    app = HawkEyeApp()
    app.mainloop()
