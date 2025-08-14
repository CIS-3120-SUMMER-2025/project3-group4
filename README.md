# AI Exercise Planner

## Overview
This project generates **custom weekly workout plans** based on a user’s **fitness goals** (e.g., strength, flexibility, endurance).  
It works by **pulling exercise data** from an external API (Ninja API) and then using **AI (Ollama)** to create a personalized, structured 7-day workout plan, all powered by [Gradio](https://www.gradio.app/)

---

## Setup & Run

### 1. **Clone Repo**
```bash
git clone <repo link>
cd <file>
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Set Environment Variables
```bash 
Create a .env file:
NINJA_API_KEY=your_api_key_here
OLLAMA_MODEL=llama3 or (llama3.2:1b in this case for RAM optimization)
``` 

### 4. Run App
```bash
python3 main.py
Gradio will open a local URL (e.g., http://127.0.0.1:7860)

Enter your fitness goal and generate your plan
```

APIs & Tools Used
API Ninjas - Exercises — Fetch exercise data

Ollama — Run AI model locally

Gradio — Simple UI for interaction

