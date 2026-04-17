import os
import datetime
from json import load, dump

from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS

load_dotenv()

# From env
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME")
USER_NAME = os.getenv("USER_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key = GROQ_API_KEY)

system = f"""
You are {ASSISTANT_NAME}, an advanced AI assistant with real-time internet access.

Provide clear, professional, and concise answers using proper grammar.
Do not add unnecessary honorifics like 'sir' unless asked.
"""

try:
    with open(r"C:\AI\My_AI\storage.json","r") as f:
        messages = load(f)
except Exception as e:
    with open(r"C:\AI\My_AI\storage.json",'w') as f:
        dump([],f)


def Googlesearch(Query):

    Answer = f"The search result for {Query} are:\n[Start]\n"

    with DDGS() as ddgs:
        results = list(ddgs.text(Query, max_results=5))  # ⭐ IMPORTANT

        for r in results:
            Answer += f"Title: {r['title']}\n"
            Answer += f"Description: {r['body']}\n\n"

    Answer += "[End]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

system_ChatBot = [

    {"role" : "system" , "content" : system},
    {"role" : "user" , "content" : "Hi"},
    {"role" : "assistant" , "content" : "Hello how can i help you?"}

]

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%I")
    minutes = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    ampm = current_date_time.strftime("%p")


    data += f"Use This Real-time information if needed:\n"
    data += f"Day : {day}\n"
    data += f"Date : {date}\n"
    data += f"Month : {month}\n"
    data += f"Year : {year}\n"
    data += f"Time : {hour} hours , {minutes} minutes ,{second} seconds.{ampm}\n"
    return data

def RealtimeSearchEngine(prompt):
    global system_ChatBot, messages

    with open(r"C:\AI\My_AI\storage.json","r") as f:
        messages = load(f)
    messages.append({"role" : "user" , "content" : f"{prompt}"})

    system_ChatBot.append({"role": "system", "content": Googlesearch(prompt)})

    response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=system_ChatBot + [{"role" : "system" , "content" : Information()}] + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )
    
    Answer = ""

    for chunk in response:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
        
    Answer = Answer.strip().replace("</s>","")
    messages.append({
    "role": "assistant",
    "content": Answer
    })


    with open(r"C:\AI\My_AI\storage.json","w") as f:
        dump(messages,f,indent=4)

    system_ChatBot.pop()
    return AnswerModifier(Answer=Answer)

