import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("cohere")

if not api_key:
    raise ValueError("❌ COHERE_API_KEY not found in environment variables")

# Initialize Cohere client
co = cohere.Client(api_key)

# Preamble (System Message)
system_prompt =  """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.

You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook', 'play song', etc.

Then you will respond with the appropriate action:

-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information or any task automation.

-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like current weather, news, stock prices, etc.

-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', 'open youtube', etc.

-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', 'close whatsapp', etc. but if the query is asking to close all apps respond with 'close all'.

-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is just asking to play music without specific song name respond with 'play music'.

-> Respond with 'generate image (image prompt)' if a query is requesting to generate an image with given prompt like 'generate image of a lion', 'create picture of sunset', etc.

-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th June for meeting', 'remind me to call mom at 5pm', etc.

-> Respond with 'system (task name)' if a query is asking to run any system command like 'shutdown', 'restart', 'sleep', 'volume up', 'volume down', etc. but if the query is asking to do multiple system tasks respond with 'system (task1, task2, task3)'.

-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else on notepad.... about a specific topic like 'write an email about resignation', 'create python script for web scraping', etc. if user mention 
   write these content on notepad respond with this content (topic)

-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics respond with 'google search (topic1, topic2, topic3)'.

-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics respond with 'youtube search (topic1, topic2, topic3)'.

-> Respond with 'web browse (url)' if a query is asking to open a specific website or webpage like 'open github.com', 'browse reddit.com', etc.

-> Respond with 'screenshot' if a query is asking to take a screenshot of the screen like 'take a screenshot', 'capture screen', etc.

-> Respond with 'calculate (mathematical expression)' if a query is asking to perform any mathematical calculation like 'what is 25 * 47', 'calculate 150 + 890', etc.

-> Respond with 'weather (location)' if a query is asking about weather of a specific location like 'weather in Delhi', 'what's the weather in New York', etc.

-> Respond with 'news (category)' if a query is asking for news about specific category like 'technology news', 'sports news', 'latest news', etc.

-> Respond with 'translate (text to language)' if a query is asking to translate text to another language like 'translate hello to Hindi', 'convert this to Spanish', etc.

-> Respond with 'timer (duration)' if a query is asking to set a timer like 'set timer for 5 minutes', 'start a 30 second timer', etc.

-> Respond with 'alarm (time)' if a query is asking to set an alarm like 'set alarm for 7:00 am', 'wake me up at 6:30', etc.

-> Respond with 'email (recipient, subject, body)' if a query is asking to send an email to someone with specific content.

-> Respond with 'read file (filename)' if a query is asking to read or open a specific file like 'read document.txt', 'open report.pdf', etc.

-> Respond with 'write file (filename, content)' if a query is asking to create or write content to a file.

-> Respond with 'download (url or file name)' if a query is asking to download something from internet.

-> Respond with 'voice command (action)' if a query is asking to perform voice-related actions like 'increase volume', 'mute', 'speak this text', etc.

*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with '(task1, task2, task3)' only open write those app which are demanded***

*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis', 'exit', 'quit', 'goodbye' respond with 'exit' ***

*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above ***

IMPORTANT: Only respond with the exact format mentioned above. Do not add any extra text, explanation or conversation. Just give the classification response.
           Think properly what is asked to open and close only open that specific application not anything else

Examples:
User: "What is the capital of France?"
Response: general ( what is the capital of france )

User: "What's the weather today?"
Response: weather ( current location )

User: "Open YouTube and play a song"
Response:( open youtube, play music )

User: "Set a reminder to call mom at 5pm tomorrow"
Response: reminder ( 5pm tomorrow - call mom )

User: "Generate an image of a mountain sunset"
Response: generate image ( mountain sunset )

user: "write a email for sick leave to HR"
Response : content (write a email for sick leave to HR)


User: "Goodbye Jarvis"
Response: exit

>>> what is capital of india open youtube , stock price of tesla and who is elon musk
Classification: ['open youtube', 'general  what is capital of india', 'realtime  stock price of tesla', 'general  who is elon musk']

>>> what is capital of india open whatsapp , stock price of tata and who is elon musk
Classification: ['open whatsapp', 'general  what is capital of india', 'realtime  stock price of tata', 'general  who is elon musk']

"""

# Build the history list starting with the System Message

funcs = [
    "open", "general", "realtime", "close", "play", "generate image",
    "reminder", "system", "content", "google search", "youtube search",
    "web browse", "screenshot", "calculate", "weather", "news",
    "translate", "timer", "alarm", "email", "read file", "write file",
    "download", "voice command", "multiple", "exit"
]

def FirstLayerDMM(prompt: str = "test"):
    try:
        messages = """[
        {"role": "system", "content:" Given},
        {"role": "user", "content": "How are you"},
        {"role": "assistant", "content": "general ( how are you )"},
        {"role": "user", "content": "do you like pizza"},
        {"role": "assistant", "content": "general ( do you like pizza )"},
        {"role": "user", "content": "Open chrome, who is mahatma gandhi"},
        {"role": "assistant", "content": "( open chrome, general who is mahatma gandhi )"},
        {"role": "user", "content": "nvidia stock price"},
        {"role": "assistant", "content": "realtime ( nvidia stock price )"} """ 

        current_chat = messages + "role : user  content  " + f"{prompt}"
        response = co.chat(
            model="command-r-plus-08-2024", 
            message=current_chat,
            preamble=system_prompt,
            temperature=0.3,
            max_tokens=200,
        )
        raw_response = ""
             
        raw_response = response.text.strip()
        raw_response = raw_response.replace("\n","")
        raw_response = raw_response.replace("(","")
        raw_response = raw_response.replace(")","")
        raw_response = raw_response.split(",")

        #print(f"Raw response: {raw_response}")  # Debug output
        
        raw_response = [i.strip() for i in raw_response]
        #print(raw_response)
        
        # Validate each task
        validated_tasks = []

        for task in raw_response:
         for func in funcs:
            if task.startswith(func):
                validated_tasks.append(task)
        
        raw_response = validated_tasks

        # If no valid tasks found, retry
        if not validated_tasks:
            print(" No valid classification found, retrying...")
            return FirstLayerDMM(prompt=prompt)
        
        return raw_response
    except Exception as e:
        print("Error :", e)
