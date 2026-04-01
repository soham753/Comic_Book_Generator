# 🦸 AI Comic Book Generator

An intelligent, Agentic AI-powered application that generates end-to-end comic book scripts, world-building overviews, and detailed image prompts. Built using **LangGraph** for advanced agent routing and **Streamlit** for a premium, interactive user experience.

## ✨ Features

- **Dynamic Story Directives:** Mix and match genres (or type your own), and select custom tones and perspectives to tailor your comic's narrative.
- **Character Management:** Easily build a custom cast of heroes, villains, and sidekicks using a sleek expander interface.
- **Live AI Progress Tracking:** Watch the AI agent build your story in real time! A sleek status logger intercepts LangGraph steps (e.g., "Generating panels," "Writing dialogue") so you have full visibility into the generation process.
- **Tabbed Results Interface:** Once generated, the comic script is neatly organized into 4 cleanly formatted tabs:
  - 📖 **Overview & World Building**
  - 🎭 **Characters**
  - 📜 **Story Phases & Panels**
  - 🖼️ **Image Prompts** (Ready to be copy/pasted into your favorite image generation AI like Midjourney or DALL-E)
- **PDF Export:** Automatically compiles your generated comic script into an easy-to-read PDF format for offline viewing or sharing.

## 🛠️ Technology Stack

- **Frontend Interface:** [Streamlit](https://streamlit.io/)
- **Agent Orchestration:** [LangGraph](https://python.langchain.com/docs/langgraph/) / LangChain
- **LLM Engine:** [Groq API](https://groq.com/) (Llama 3 / Mixtral models for ultra-fast inference)

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python installed. It is recommended to use a virtual environment (`venv`).

### 2. Install Dependencies
Install the required packages:
```bash
pip install streamlit langchain langgraph pandas python-dotenv
```
*(Also ensure any specific LLM integration libraries like `langchain-groq` or local node scripts in your project are satisfied).*

### 3. Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_api_key_here
LANGSMITH_API_KEY=optional_langsmith_key
LANGCHAIN_TRACING_V2=true
```
*Note: You can also enter the Groq API key directly via the Streamlit UI Sidebar.*

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
This will open the application in your default web browser (usually at `http://localhost:8501`).

## 📁 Repository Structure
- `app.py`: The main Streamlit entry point, featuring custom CSS and UI logic.
- `graph/`: Contains the core LangGraph logic and routing for the AI agent.
- `nodes/`: Contains individual step definitions for the AI (story outlining, panel generation, dialogue writing).
- `loggerConfig/`: Contains a custom logging handler (`StreamlitLogHandler`) that pipes agent progress directly into the Streamlit UI.
- `pdfmaker.py`: A utility script that parses the AI's `story.json` output and formats it into a downloadable PDF.

---
*Built with ❤️ utilizing Agentic AI workflows.*