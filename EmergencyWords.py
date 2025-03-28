import speech_recognition as sr
import settings
import MicActive as ma

def detect_emergency_words(event):
    """Detects emergency words using speech recognition and triggers emergency event."""
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("[EMG] Listening for emergency words...")
        recognizer.adjust_for_ambient_noise(source)

        while not event.is_set():  # Stop immediately if triggered
            try:
                if event.is_set():
                    print("[EMG] Emergency already triggered! Stopping word detection.")
                    break  
                print("Listening...")

                if not settings.DEBUG1:
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio).lower()
                else:
                    text = "help"

                print(f"[EMG] Detected: {text}")

                for word in settings.emergency_words:
                    if word in text:
                        print("[EMG] Emergency word detected! Activating Security System...")
                        event.set()
                        return

            except sr.UnknownValueError:
                if not settings.DEBUG1:
                    if ma.decibels[0] >= 35:
                        print("[EMG] Could not understand the audio.")
            except sr.RequestError:
                if not settings.DEBUG1:
                    print("[EMG] Speech Recognition API error.")
            except KeyboardInterrupt:
                print("[EMG] Stopping detection...")
                break

    print("[EMG] Emergency words detection stopped.")
