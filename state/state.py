from typing import TypedDict, List, Dict, Optional,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class ComicState(TypedDict):

    user_input: Dict 

    story_title: Optional[str]
    story_overview: Optional[str]
    story_phases: Optional[List[Dict]]
    current_phase_index: Optional[int]
    current_phase: Optional[Dict]

    panels: Optional[List[Dict]]
    comic_pages: Optional[List[Dict]]

    world_building:Optional[str]
    character:Optional[List[Dict]]
    character_image_generation_prompt: Optional[List[Dict]]
    character_image_prompts: Optional[List[str]]
    current_character_index: Optional[int]
    current_character: Optional[Dict]

    comic_page_image_prompts: Optional[List[str]]
