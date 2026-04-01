import streamlit as st
import os
import pandas as pd
import json
import subprocess
import logging
from dotenv import load_dotenv
from llm.groq import GroqLLM
from graph.graph import ComicGraph
from loggerConfig.logger_config import setup_logger

class StreamlitLogHandler(logging.Handler):
    def __init__(self, st_container):
        super().__init__()
        self.st_container = st_container
        self.logs = []
        
    def emit(self, record):
        msg = record.getMessage()
        # Only capture the clean "Generating..." steps to show the user
        if msg.startswith("Generating") or msg.startswith("Started"):
            # Make it more readable
            clean_msg = msg.replace("number of phase: ", "Phase ")
            clean_msg = clean_msg.replace("comic page image generation prompt", "image prompts")
            if clean_msg not in self.logs:
                self.logs.append(clean_msg)
            
            # Show a nice clean list of steps
            # The last item gets a loading hourglass, previous items get a checkmark
            bullet_points = "\n".join(f"- ✅ {log}" if i < len(self.logs)-1 else f"- ⏳ {log}" for i, log in enumerate(self.logs[-10:]))
            self.st_container.markdown(bullet_points)

# Load environment variables
load_dotenv()
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
setup_logger()

# Setup App
st.set_page_config(page_title="AI Comic Generator", layout="wide", page_icon="🦸")

# Modern Premium UI Styling
st.markdown("""
<style>
.main-header {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 0px;
}
.sub-header {
    font-size: 1.2rem;
    color: #8C92AC;
    margin-top: -10px;
    margin-bottom: 2rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
}
.stButton>button {
    width: 100%;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🦸 AI Comic Book Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Craft stunning comic narratives and visual prompts utilizing a LangGraph agent!</p>', unsafe_allow_html=True)

# Sidebar - Configuration
st.sidebar.markdown("### 🔑 API Settings")
groq_api_key_input = st.sidebar.text_input("Groq API Key", type="password", help="Enter your Groq API key here. It overrides the .env key.")
st.sidebar.divider()

st.sidebar.markdown("### ⚙️ Story Directives")

# Genre
genre_options = ["Superhero", "Sci-Fi", "Fantasy", "Horror", "Cyberpunk", "Mystery", "Other"]
genre_selections = st.sidebar.multiselect("Genre", genre_options, default=["Superhero"])
final_genre_list = [g for g in genre_selections if g != "Other"]
if "Other" in genre_selections:
    custom_genre = st.sidebar.text_input("Custom Genre", placeholder="e.g. Noir, Space Opera")
    if custom_genre:
        final_genre_list.append(custom_genre)
genre = ", ".join(final_genre_list) if final_genre_list else "Superhero"

# Tone
tone_options = ["Exciting and Humorous", "Dark and Gritty", "Lighthearted", "Suspenseful", "Epic", "Other"]
tone_selection = st.sidebar.selectbox("Tone", tone_options)
tone = tone_selection
if tone_selection == "Other":
    tone = st.sidebar.text_input("Custom Tone", value="Dramatic")

# Perspective
perspective_options = ["First-person", "Third-person", "Omniscient", "Other"]
perspective_selection = st.sidebar.selectbox("Perspective", perspective_options)
perspective = perspective_selection
if perspective_selection == "Other":
    perspective = st.sidebar.text_input("Custom Perspective", value="Second-person")

# Main Content Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🌎 World Building")
    setting = st.text_area("Setting & Environment", "A futuristic cyberpunk city at night with glowing skyscrapers and flying vehicles.", height=120)

with col2:
    st.markdown("### 🎭 Cast of Characters")
    if 'characters' not in st.session_state:
        st.session_state['characters'] = [
            {"name": "Arjun", "role": "Hero", "description": "a young engineer who can control electricity"},
            {"name": "Shadow Vex", "role": "Villain", "description": "a mysterious hacker wearing a black cloak and neon mask"}
        ]
        
    for i, char in enumerate(st.session_state['characters']):
        with st.expander(f"👤 {char['name'] or 'New Character'} ({char['role']})", expanded=False):
            st.session_state['characters'][i]['name'] = st.text_input(f"Name", char['name'], key=f"name_{i}")
            st.session_state['characters'][i]['role'] = st.text_input(f"Role", char['role'], key=f"role_{i}")
            st.session_state['characters'][i]['description'] = st.text_area(f"Description", char['description'], key=f"desc_{i}")
            if st.button("❌ Remove Character", key=f"del_{i}", use_container_width=True):
                st.session_state['characters'].pop(i)
                st.rerun()

    if st.button("➕ Add New Character", use_container_width=True):
        st.session_state['characters'].append({"name": "Unnamed", "role": "Sidekick", "description": ""})
        st.rerun()

st.markdown("<br/>", unsafe_allow_html=True)

# Generation Execution
if st.button("🚀 IGNITE: Generate Comic Script", type="primary"):
    active_api_key = groq_api_key_input if groq_api_key_input else os.environ.get("GROQ_API_KEY", "")
    if not active_api_key:
        st.error("Please enter a Groq API Key in the sidebar or ensure GROQ_API_KEY is placed in your .env file.")
        st.stop()

    os.environ["GROQ_API_KEY"] = active_api_key

    with st.status("🤖 Agent is architecting your story...", expanded=True) as status:
        log_box = st.empty()
            
        # Hook custom logger
        root_logger = logging.getLogger()
        streamlit_handler = StreamlitLogHandler(log_box)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        streamlit_handler.setFormatter(formatter)
        root_logger.addHandler(streamlit_handler)

        try:
            llm = GroqLLM().get_model()
            comic_graph = ComicGraph(llm)
            graph = comic_graph.graph_builder.compile()

            user_input = {
                "genre": genre,
                "tone": tone,
                "perspective": perspective,
                "setting": setting,
                "characters": st.session_state['characters']
            }

            result = graph.invoke({"user_input": user_input})
            
            story = {
                "story_title": result.get("story_title", "Untitled"),
                "story_overview": result.get("story_overview", ""),
                "story_phases": result.get("story_phases", []),
                "world_building": result.get("world_building", ""),
                "character": result.get("character", []),
                "comic_page_image_prompts": result.get("comic_page_image_prompts", []),
            }

            # Save to JSON
            pd.DataFrame([story]).to_json("story.json")
            
            # Generate PDF
            status.update(label="✅ Script Generated! Compiling PDF...", state="running")
            subprocess.run(["python", "pdfmaker.py"], check=True)

            status.update(label="🎉 Comic Book generated successfully!", state="complete", expanded=False)

            # Store result in session state to show them
            st.session_state['final_story'] = story
            
        except Exception as e:
            status.update(label="❌ An error occurred during generation.", state="error", expanded=True)
            st.error(str(e))
        finally:
            root_logger.removeHandler(streamlit_handler)


# Result Display using Sleek Tabs
if 'final_story' in st.session_state:
    story = st.session_state['final_story']
    st.divider()
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"## 📚 {story['story_title']}")
    with col_b:
        if os.path.exists("story_output.pdf"):
            with open("story_output.pdf", "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF Script",
                    data=file,
                    file_name="comic_story.pdf",
                    mime="application/pdf",
                    type="secondary",
                    use_container_width=True
                )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🎭 Characters", "📜 Story Panels", "🖼️ Prompts"])
    
    with tab1:
        st.markdown("### Synopsis")
        st.info(story["story_overview"])
        st.markdown("### Built World")
        st.success(story["world_building"])
        
    with tab2:
        for char in story.get("character", []):
            st.markdown(f"**{char.get('name', 'Unknown')}**")
            st.write(f"*{char.get('description', '')}*")
            st.caption(f"Looks: {char.get('looks', '')} | Personality: {char.get('personality', '')}")
            st.divider()

    with tab3:
        st.json(story["story_phases"])

    with tab4:
        for i, prompt in enumerate(story["comic_page_image_prompts"]):
            st.markdown(f"##### Page {i+1}")
            st.code(prompt, language='text')
