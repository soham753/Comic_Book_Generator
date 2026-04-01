from pydantic import BaseModel, Field
from typing import List, Optional


class Dialogue(BaseModel):
    character: str
    text: str


class PanelDialogue(BaseModel):
    panel_number: int
    dialogue: List[Dialogue] = Field(default_factory=list)
    caption: Optional[str] = None


class DialogueOutline(BaseModel):
    panels: List[PanelDialogue]