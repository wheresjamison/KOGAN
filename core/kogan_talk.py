import sounddevice as sd
import queue
import sys
import json
import os
import requests
import tempfile
from datetime import datetime, timedelta
from TTS.api import TTS
from faster_whisper import WhisperModel
from scipy.io.wavfile import write as wav_write

# Set up paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
long_term_memory_path = os.path.join(BASE_DIR, "../data/long_term_memory.json")
token_path = os.path.join(BASE_DIR, "../token_expiry.txt")

# Ensure memory file and folder exist
if not os.path.exists(os.path.dirname(long_term_memory_path)):
    os.makedirs(os.path.dirname(long_term_memory_path), exist_ok=True)
if not os.path.exists(long_term_memory_path):
    with open(long_term_memory_path, "w") as f:
        json.dump([], f)

# Set up Whisper (STT)
whisper_model = WhisperModel("base", compute_type="int8")

def transcribe_audio(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments])

# Set up TTS (Text to Speech)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# Initialize conversation memory
conversation_history = []

# Intent tagging logic
def detect_intent(text):
    keywords = {
        "food": ["favorite food", "like to eat", "love sushi", "pizza", "burgers"],
        "name": ["my name is", "call me", "i am"],
        "location": ["live in", "from", "located"],
        "preference": ["i like", "i prefer", "my favorite", "favorite color"]
    }
    tags = []
    lowered = text.lower()
    for intent, phrases in keywords.items():
        if any(p in lowered for p in phrases):
            tags.append(intent)
    return tags

def append_to_long_term_memory(user_input, assistant_reply):
    try:
        with open(long_term_memory_path, "r") as f:
            memory = json.load(f)
        memory.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "kogan": assistant_reply,
            "tags": detect_intent(user_input)
        })
        with open(long_term_memory_path, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"Error saving to long-term memory: {e}")

def check_token_expiry():
    try:
        with open(token_path, "r") as f:
            expiry_str = f.read().strip()
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
            today = datetime.now()
            days_left = (expiry_date - today).days

            if 0 < days_left <= 7:
                return f"Reminder: Your GitHub token will expire in {days_left} day(s). Consider renewing it soon."
            elif days_left <= 0:
                return "Alert: Your GitHub token has expired. Please generate a new one."
            else:
                return None
    except Exception:
        return None

def recall_relevant_memory():
    try:
        with open(long_term_memory_path, "r") as f:
            memory = json.load(f)
        preferences = [entry for entry in memory if "preference" in entry.get("tags", [])]
        if preferences:
            return "\n".join([f"Previously you said: \"{entry['user']}\"" for entry in preferences[-2:]])
        return ""
    except Exception as e:
        return ""

def listen_and_respond():
    print("🎤 Say something to KOGAN...")
    duration = 5  # seconds
    samplerate = 16000
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        print("⏺️ Recording...")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        print("📼 Saving audio...")
        wav_write(tmp.name, samplerate, recording)

        print("🧠 Transcribing...")
        text = transcribe_audio(tmp.name)
        print(f"🧾 Whisper heard: {text}")

        if text:
            conversation_history.append({"role": "user", "content": text})
            reply = generate_response(text)
            conversation_history.append({"role": "assistant", "content": reply})
            append_to_long_term_memory(text, reply)
            speak(reply)

def generate_response(prompt):
    try:
        reminder = check_token_expiry()
        recalled = recall_relevant_memory()

        context = "\n".join([
            f"User: {entry['content']}" if entry['role'] == "user" else f"KOGAN: {entry['content']}"
            for entry in conversation_history[-6:]
        ])

        reminder_text = (reminder + "\n") if reminder else ""
        recall_text = (recalled + "\n") if recalled else ""

        system_instructions = (
            "You are KOGAN, an AI assistant with short-term and long-term memory. "
            "You remember previous user inputs across sessions. Use prior memories if relevant.\n"
        )

        full_prompt = f"{reminder_text}{recall_text}{system_instructions}{context}\nUser: {prompt}\nKOGAN:"
        print("🧾 Final prompt sent to model:\n", full_prompt)

        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "openchat",
            "prompt": full_prompt,
            "stream": False
        })
        response = res.json().get("response", "I'm not sure how to respond to that.")
        return response
    except Exception as e:
        return f"Error: {e}"

def speak(text):
    print(f"💬 KOGAN says: {text}")
    text = text.strip().replace("\n", " ").replace("  ", " ")
    if len(text) > 300:
        text = text[:297] + "..."
    tts.tts_to_file(text=text, file_path="response.wav")
    os.system("aplay response.wav")

if __name__ == "__main__":
    listen_and_respond()

