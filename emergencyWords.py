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
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio).lower()
            if DEBUG:
                print(f"Detected: {text}")

            for word in EMERGENCY_WORDS:
                if word in text:
                    if DEBUG:
                        print("Emergency word detected!")
                    return True
            
    return False

if DEBUG:
    detect_emergency_words()
