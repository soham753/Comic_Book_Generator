from pydantic import BaseModel
from typing import List


class ComicPageGenerationSchema(BaseModel):
    prompt: str = ""