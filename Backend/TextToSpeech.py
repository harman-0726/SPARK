import os
import time
import pygame
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("ELEVENLABS_API_KEY missing")

client = ElevenLabs(api_key=API_KEY)

def Generate(text):

    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id="pNInz6obpgDQGcFmaJgB",
        model_id="eleven_flash_v2"
    )
    
    audio_file = "jarvis.mp3"
    with open(audio_file, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.quit()
