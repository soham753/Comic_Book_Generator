from pydantic import BaseModel
from typing import List, Optional


class Dialogue(BaseModel):
    character: str
    text: str


class Panel(BaseModel):
    panel_number: int
    camera_shot: str
    action: str
    characters: List[str]

    dialogue: Optional[List[Dialogue]] = []
    caption: Optional[str] = None


class PanelOutline(BaseModel):
    panels: List[Panel]