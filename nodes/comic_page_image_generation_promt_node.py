from langchain_core.messages import SystemMessage, HumanMessage
from prompts.comic_page_image_generation_prompt import ComicPageImageGenerationPrompt
from schemas.comic_page_generation_schema import ComicPageGenerationSchema
import logging

logger = logging.getLogger(__name__)



class ComicPageImageGenerationPromptNode:

    def __init__(self, llm):
        self.llm = llm
        self.prompt = ComicPageImageGenerationPrompt()

    def run(self, state):
        logger.info(f"Generating comic page image generation prompt for number of phase: {state['current_phase_index'] + 1}")

        phase = state["current_phase"]
        panels = state["panels"]

        response = self.llm.invoke([
            SystemMessage(content=self.prompt.system_prompt),
            HumanMessage(
                content=f"""
generate comic page image generation prompt for the following comic panels.

core character:
{state["character"]}

Panels:
{panels}
IMPORTANT: Output MUST be **exact valid JSON only**, no extra text, comments, or markdown.
Format:
{{
  "prompt": "your generated prompt string "
}}
"""
            )
        ])

        comic_page_image_generation_prompt = state.get("comic_page_image_prompts", [])
        comic_page_image_generation_prompt.append("Generate comic page image for the following comic panels.\n\n" + response.content)
        logger.info(f"Comic page image generation prompt generated successfully for phase: {state['current_phase_index'] + 1}")
        return {
            "comic_page_image_prompts": comic_page_image_generation_prompt
        }