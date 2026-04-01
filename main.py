import os
from dotenv import load_dotenv
from llm.groq import GroqLLM
from graph.graph import ComicGraph
import pandas as pd
from loggerConfig.logger_config import setup_logger


load_dotenv()
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
setup_logger()
llm = GroqLLM().get_model()
comic_graph = ComicGraph(llm)
graph = comic_graph.graph_builder.compile()


user_input = {
    "genre": "superhero",
    "tone": "exciting and humorous",
    "perspective": "third-person",
    "setting": "a futuristic city at night with glowing skyscrapers and flying vehicles",
    "characters": [
        {
            "name": "Arjun",
            "role": "hero",
            "description": "a young engineer who can control electricity"
        },
        {
            "name": "Shadow Vex",
            "role": "villain",
            "description": "a mysterious hacker wearing a black cloak and neon mask"
        }
    ]
}
result = graph.invoke({"user_input": user_input})
story = {
    "story_title":result["story_title"],
    "story_overview":result["story_overview"],
    "story_phases":result["story_phases"],
    "world_building":result["world_building"],
    "character":result["character"],
    "comic_page_image_prompts":result["comic_page_image_prompts"],
}

data = pd.DataFrame([story])

data.to_json("story.json") 
