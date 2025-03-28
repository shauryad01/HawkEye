import threading
import numpy as np
import settings
import keyboard
import random
if not settings.DEBUG1:
    import sounddevice as  sd

settings.emergency_triggered=threading.Event()
global decibels
decibels = [0]

def debug1_mode():
    """ Simulates microphone activity when DEBUG1 is enabled. """
    while not settings.emergency_triggered.is_set():
        simulated_decibels = random.uniform(55, 65)  # Random float between 55-65 dB
        print(f"Current Volume: {simulated_decibels:.2f} dB")  
        
        if simulated_decibels >= settings.MIC_SENSITIVITY_THRESHOLD:
            settings.emergency_triggered.set()
            print("[VOL] Security system activated by simulated volume!")

        if keyboard.is_pressed('q'):
            print("Exiting...")
            break

def get_volume(event):
    
    def callback(indata, frames, time, status):
        if event.is_set():
            return
                    
        rms = np.sqrt(np.mean(indata**2))  # Compute RMS
        decibels = 20 * np.log10(max(rms, 1e-10)) + 96.3  # Convert to dB
                
        if settings.DEBUG or settings.DEBUG1:
            print(f"Decibels: {decibels[0]:.2f} dB")
        
        if decibels >= settings.MIC_SENSITIVITY_THRESHOLD:
            event.set()
            print("Security system activated by volume")
            return True


    if not settings.DEBUG1:
        with sd.InputStream(callback=callback):
            while not settings.emergency_triggered.is_set():
                pass


if settings.DEBUG1:
    debug1_mode()
elif settings.DEBUG:
    get_volume()