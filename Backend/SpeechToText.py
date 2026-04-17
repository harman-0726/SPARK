# pyright: reportAttributeAccessIssue=false
import speech_recognition as sr
import pyttsx3 as p
import time
import queue
import threading

r = sr.Recognizer()
r.pause_threshold = 2

engine = p.init()
listening = True

query_queue = queue.Queue()

def listen():
    while True:
        
        try:
            if not listening:
                time.sleep(0.1)
                continue

            with sr.Microphone() as source:
                if not listening:
                    continue
                print("🎤 Listening...")

                r.adjust_for_ambient_noise(source, duration=0.3)
                audio = r.listen(source)

                # type: ignore
                text = r.recognize_google(audio, language="en-IN")
                final_query = text
                query_queue.put(final_query)
    
        except sr.UnknownValueError:
            print("Did not hear properly")
        except sr.RequestError:
            print("Network issue")

def Listen():
    threading.Thread(target=listen,daemon=True).start()

def resume_listening():
    global listening
    listening = True

def pause_listening():
    global listening
    listening = False