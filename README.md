# KOGAN — Modular AI Assistant on Edge Hardware

**KOGAN** is a voice-powered, offline-capable AI assistant engineered for real-world usability, privacy, and extensibility. Designed to replace mainstream smart assistants (e.g., Bixby, Google Assistant, Alexa), KOGAN operates independently on a secured Linux-based edge device with full voice interaction, conversational intelligence, and modular features.

---

## 🔧 Key Features

- **Offline Speech Recognition (STT):** Real-time transcription using Vosk
- **Natural Language Understanding:** Local LLM integration (e.g., Gemma via Ollama)
- **Text-to-Speech (TTS):** Voice synthesis with Coqui TTS
- **Conversational Context Memory:** Remembers dialogue across turns (in development)
- **Version Awareness:** Self-identifies version via internal tracking
- **Secure Remote Access:** SSH-enabled, with Git integration for rollback and recovery
- **Modular Design:** Components are loosely coupled for flexibility and future integrations

---

## 🧠 Architecture

```text
┌──────────────┐      ┌────────────┐      ┌────────────┐
│ Mic Input    │─────▶│ Vosk STT   │─────▶│ LLM Engine │
└──────────────┘      └────────────┘      └────┬───────┘
                                               │
                                  ┌────────────▼────────────┐
                                  │ Contextual Response Gen │
                                  └────────────┬────────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │ Coqui TTS (Speech)  │
                                    └──────────┬──────────┘
                                               │
                                          ┌────▼────┐
                                          │ Speaker │
                                          └─────────┘

---

## 🔐 Privacy & Control

This project was built with privacy as a core value. No user data, personal credentials, financial information, or prior conversations are tracked, stored, or shared. GitHub is used strictly for version control and code development. KOGAN runs entirely under user control on a local machine.

---

## ⚙️ Development Stack

- OS: Ubuntu / Pop!_OS (64-bit)  
- Language: Python 3.11  
- Key Tools: `vosk`, `sounddevice`, `TTS`, `ollama`, `requests`, `git`  
- Version Control: Git (with custom `VERSION` file)  
- Deployment: Local laptop with 11.6 GiB RAM, Intel i7 CPU  

---

## 🧩 Example Use Cases

- Daily voice assistant with no cloud dependency  
- Secure command-line control over home systems  
- Modular base for building a private smart home stack  
- Demonstration of offline LLM workflows  

---

## 🚧 In Progress

- 🔄 Persistent memory (local file-based conversation context)  
- 🧠 Self-editing code routines based on natural language prompts  
- 📅 Calendar and to-do list syncing  
- 🛒 Amazon cart building, weather-based outfit suggestions  

---

## 👨‍💻 Creator

This project is maintained privately for personal use and technical demonstration purposes. Designed for learning, iteration, and showcasing autonomous assistant architecture without reliance on third-party ecosystems.
=======
# KOGAN
Voice-driven offline AI assistant running on Linux, integrating Vosk, Coqui TTS, and LLMs (Ollama/Gemma) with modular features, version control, and secure remote access. Designed for real-world, customizable smart assistant use — no cloud dependency required.
