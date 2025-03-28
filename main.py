import multiprocessing as mp
import MicActive as ma
import CamActive as ca
import EmergencyWords as ew
import settings
import cv2
import time

# Initialize the emergency trigger event
settings.emergency_triggered = mp.Event()

def camera_stream(event):
    print("[CAM] Camera process started")
    ca.cam_active(event)


# Function for volume detection
def volume_stream(event):
    time.sleep(2)
    print("[VOL] Starting volume detection...")
    ma.get_volume(event)

# Function for emergency word detection
def emergency_stream(event):
    time.sleep(2)
    print("[EMG] Starting emergency word detection...")
    ew.detect_emergency_words(event)


# Main function to start processes
def main():
    # Create processes for tasks
    camera_process = mp.Process(target=camera_stream, args=(settings.emergency_triggered,), daemon=True)
    volume_process = mp.Process(target=volume_stream, args=(settings.emergency_triggered,), daemon=True)
    emergency_process = mp.Process(target=emergency_stream, args=(settings.emergency_triggered,), daemon=True)

    # Start Processes
    camera_process.start()
    volume_process.start()
    emergency_process.start()

    print("[MAIN] All processes started.")

    # Monitor the emergency event in the main thread
    while not settings.emergency_triggered.is_set():
        time.sleep(0.5)

    print("[MAIN] Emergency triggered! Stopping all processes...")

    # Stop all processes when emergency is triggered
    camera_process.terminate()
    volume_process.terminate()
    emergency_process.terminate()

    # Wait for processes to finish
    camera_process.join()
    volume_process.join()
    emergency_process.join()

    print("[MAIN] Program exited.")

if __name__ == "__main__":
    main()
