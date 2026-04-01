from pydantic import BaseModel
from typing import List


class CharacterImageGenerationPromptSchema(BaseModel):
    prompt:str