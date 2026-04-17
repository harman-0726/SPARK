
# ⚡ Spark — Personal AI Assistant

> Voice-powered AI assistant built with Python. Listens, thinks, and responds using real-time speech recognition, LLM inference, and text-to-speech — with an animated orb GUI that reacts live to every state.

---

## 🎥 Demo

> Orb pulses blue when listening, spins purple when thinking, morphs when speaking.

---

## 🧠 Features

- 🎤 **Voice Input** — Continuous speech recognition via Google Speech API
- 🤖 **Smart Classification** — Cohere AI routes queries to the right handler
- 💬 **Conversational AI** — Groq (LLaMA 3.3 70B) for general chat with memory
- 🌐 **Real-time Search** — DuckDuckGo search + Groq for live answers
- 🔊 **Voice Output** — ElevenLabs text-to-speech
- 🖥️ **Automation** — Open/close apps, take screenshots, write content to Notepad
- 🔵 **Animated Orb GUI** — Live orb that reacts to every assistant state

---

## 🏗️ Architecture

```
User Voice
    │
    ▼
SpeechToText.py         ← Microphone → Google STT
    │
    ▼
Classifier.py           ← Cohere → routes to correct handler
    │
    ├── General.py       ← Groq LLaMA (chat + memory)
    ├── realtime.py      ← DuckDuckGo + Groq (live search)
    └── Automation.py    ← App control, screenshots, Notepad
    │
    ▼
TextToSpeech.py         ← ElevenLabs TTS
    │
    ▼
GUI.py + orb.html       ← Flask-SocketIO live orb
```

---

## 📁 Project Structure

```
Spark/
├── Backend/
│   ├── Brain.py          # Main loop — orchestrates everything
│   ├── Classifier.py     # Query classification (Cohere)
│   ├── General.py        # Conversational AI (Groq + memory)
│   ├── realtime.py       # Real-time search engine
│   ├── Automation.py     # System automation tasks
│   ├── SpeechToText.py   # Voice input (threaded listener)
│   ├── TextToSpeech.py   # Voice output (ElevenLabs)
│   └── GUI.py            # Flask-SocketIO state server
├── Frontend/
│   └── orb.html          # Animated orb interface
├── .env                  # API keys (not committed)
└── storage.json          # Conversation memory
```

---

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/spark-ai.git
cd spark-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

```env
GROQ_API_KEY=your_groq_key
ELEVENLABS_API_KEY=your_elevenlabs_key
cohere=your_cohere_key
USER_NAME=YourName
ASSISTANT_NAME=Spark
```

### 4. Run

```bash
python Backend/Brain.py
```

The orb GUI opens automatically in your browser. Say something — Spark is listening.

---

## 📦 Requirements

```
speechrecognition
pyaudio
groq
cohere
elevenlabs
flask
flask-socketio
pygame
python-dotenv
ddgs
pyautogui
AppOpener
```

---

## 🗣️ Example Commands

| You say | Spark does |
|--------|-----------|
| "What is quantum computing?" | Answers via LLaMA |
| "What's the latest news on Tesla?" | Searches web + summarizes |
| "Open YouTube" | Launches YouTube |
| "Take a screenshot" | Captures screen |
| "Write an email for sick leave" | Types in Notepad via AI |
| "Goodbye" | Exits cleanly |

---

## 🔑 API Keys Needed

| Service | Free Tier | Link |
|---------|-----------|------|
| Groq | ✅ Yes | [console.groq.com](https://console.groq.com) |
| Cohere | ✅ Yes | [cohere.com](https://cohere.com) |
| ElevenLabs | ✅ Yes (limited) | [elevenlabs.io](https://elevenlabs.io) |

---

## ⚙️ How It Works

1. `SpeechToText.py` runs a background thread, continuously listening via microphone
2. On speech detected, `Brain.py` pauses the listener and classifies the query via Cohere
3. The classified task routes to `General`, `realtime`, or `Automation`
4. Response is spoken aloud via ElevenLabs
5. The orb GUI updates in real time via WebSocket for each state change

---

## 🛣️ Roadmap

- [ ] Wake word detection ("Hey Spark")
- [ ] Image generation support
- [ ] WhatsApp/Email automation
- [ ] System volume/brightness control
- [ ] Multi-language support

---

## 👤 Author

Built by **[Your Name]** — feel free to fork, star ⭐, and contribute.

---

## 📄 License

MIT License
