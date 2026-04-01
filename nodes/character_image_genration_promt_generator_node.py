import json
from langchain_core.messages import SystemMessage, HumanMessage
from schemas.character_image_generation_prompt_schema import CharacterImageGenerationPromptSchema
from prompts.character_image_genaration_prompt_generation_prompt import CharacterImageGenerationPromptGenerationPrompt
import logging

logger = logging.getLogger(__name__)



class CharacterImageGenerationPromptGeneratorNode:

    def __init__(self, llm):
        self.llm = llm
        self.character_image_generation_prompt = CharacterImageGenerationPromptGenerationPrompt()

    def character_image_generation_prompt_generator_node(self, state):
        logger.info(f"Generating character image generation prompt for character: {state['current_character_index'] + 1}")
        character = state["current_character"]
        world = state.get("world_building", "")
        overview = state.get("story_overview", "")

        # Serialize character as JSON string
        character_json = json.dumps(character)

        response = self.llm.invoke([
            SystemMessage(content=self.character_image_generation_prompt.system_prompt),
            HumanMessage(
                content=f"""
Generate an AI image prompt for this character.
Character details (as JSON string):
{character_json}
Story world description:
{world}
Story overview:
{overview}

Return ONLY the raw string prompt text describing the character. Do NOT wrap it in JSON.
"""
            )
        ])
        prompts = state.get("character_image_prompts", [])

        # Extract the JSON field from structured output
        prompt = response.content
        prompts.append(prompt)
        logger.info(f"Character image generation prompt generated successfully for character: {state['current_character_index'] + 1}")
        return {
            "character_image_prompts": prompts
        }



