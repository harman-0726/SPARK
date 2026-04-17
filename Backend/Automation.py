from AppOpener import open, close
import os
import webbrowser
import pyautogui
import time
from General import chatBot


def write_in_notepad(text):

    # open notepad
    open("notepad")
    time.sleep(2)

    # generate AI content
    content = chatBot(text)

    # type automatically
    pyautogui.write(content, interval=0.02)


def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    image = pyautogui.screenshot()
    image.save(filename)
    return "Screenshot captured, sir."


def Auto_task(query):

    try:
        for task in query:

            task = task.lower()

            if "open" in task:

                if "whatsapp" in task:
                    open("whatsapp")

                elif "file manager" in task or "explorer" in task:
                    open("File Explorer")

                elif "notepad" in task:
                    open("notepad")

                elif "gmail" in task:
                    webbrowser.open("https://mail.google.com")

                elif "youtube" in task:
                    webbrowser.open("https://youtube.com")

                elif "linkedin" in task:
                    webbrowser.open("https://linkedin.com")

                elif "github" in task:
                    webbrowser.open("https://github.com")

                elif "chatgpt" in task:
                    webbrowser.open("https://chat.openai.com")

                elif "stack overflow" in task:
                    webbrowser.open("https://stackoverflow.com")

        
            elif "close" in task:

                if "whatsapp" in task:
                    os.system("taskkill /f /im WhatsApp.exe")

                elif "notepad" in task:
                    os.system("taskkill /f /im notepad.exe")

                elif "file manager" in task:
                    close("File Explorer")

            elif "screenshot" in task:
                return take_screenshot()

            elif "content" in task:
                topic = task.replace("content", "").strip()
                write_in_notepad(topic)
                return "Writing completed in Notepad, sir."

    except Exception as e:
        print("Automation Error:", e)

    return "Task completed, sir."
