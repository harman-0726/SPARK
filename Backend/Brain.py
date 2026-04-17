import time
import threading
import webbrowser
 
from Classifier import FirstLayerDMM
from SpeechToText import Listen, query_queue, pause_listening, resume_listening
from General import chatBot
from realtime import RealtimeSearchEngine
from Automation import Auto_task
from TextToSpeech import Generate
from GUI import run, set_state
 
def clean_text(text):
    # remove markdown symbols
    text = text.replace("**", "")
    text = text.replace("*", "")
    text = text.replace("__", "")
    text = text.replace("`", "")
    return text
 
def execute_task(tasks):
 
    final_response = ""
    
 
    for task in tasks:
 
        # GENERAL
        if task.startswith("general"):
            query = task.replace("general", "").strip()
            final_response = clean_text(chatBot(query))
 
        #  REALTIME 
        elif task.startswith("realtime"):
            query = task.replace("realtime", "").strip()
            final_response = clean_text(RealtimeSearchEngine(query))
 
        # AUTOMATION 
        elif (
            task.startswith("open")
            or task.startswith("close")
            or task.startswith("screenshot")
            or task.startswith("content")
        ):
            result = Auto_task([task])
            final_response = result
 
        # EXIT 
        elif task in ["exit", "sleep", "rest"]:
            Generate("Goodbye sir.")
            exit()
 
    return final_response
 
 
if __name__ == "__main__":
 
    print("Spark Brain Online, sir.")
 
    # Start GUI server in background
    threading.Thread(target=run, daemon=True).start()
 
    # Open browser after short delay
    time.sleep(1.5)
    webbrowser.open("http://localhost:5000")
 
    Listen()
    set_state("listening")
 
    while True:
 
        if not query_queue.empty():
 
            query = query_queue.get().lower().strip()
 
            pause_listening()
            set_state("thinking")
 
            print("USER:", query)
 
            tasks = FirstLayerDMM(query)
 
            response = execute_task(tasks)
 
            if response:
                print("SPARK:", response)
                set_state("speaking")
                Generate(response)
 
            resume_listening()
            set_state("listening")
 
        time.sleep(0.1)