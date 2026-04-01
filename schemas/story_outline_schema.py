from pydantic import BaseModel
from typing import List


class StoryPhase(BaseModel):
    phase_number: int
    phase_title: str
    description: str
    characters: List[str]

class Character(BaseModel):
    name: str
    description: str
    looks: str
    personality: str
    gender:str
    age:str

class StoryOutline(BaseModel):
    story_title: str
    story_overview: str
    characters: List[Character]
    world_building: str
    story_phases: List[StoryPhase]