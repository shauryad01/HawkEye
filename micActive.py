import pyaudio
import audioop
import keyboard
import math
import time

DEBUG = False
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def get_volume():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)

        while True:
            audio_data = stream.read(CHUNK, exception_on_overflow=False)  
            rms = audioop.rms(audio_data, 2)
            decibels = 20 * math.log10(rms) if rms > 0 else 0
            # print(f"Decibels: {decibels:.2f} dB")

            if keyboard.is_pressed('q'):
                print("Exiting...")
                break
            
            time.sleep(0.003)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        return decibels

if DEBUG:
    get_volume()
