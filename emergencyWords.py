import speech_recognition as sr

DEBUG = True

EMERGENCY_WORDS = {"help", "stop"}

def detect_emergency_words():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for emergency words...")
        recognizer.adjust_for_ambient_noise(source)
        while True:     
            try:       
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                text = recognizer.recognize_google(audio).lower()
                if DEBUG:
                    print(f"Detected: {text}")

                for word in EMERGENCY_WORDS:
                    if word in text:
                        print("Emergency word detected!")
                        return True
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError:
                print("Speech Recognition API error.")
            except KeyboardInterrupt:
                print("Stopping detection...")
                break
            
    return False

if DEBUG:
    detect_emergency_words()
