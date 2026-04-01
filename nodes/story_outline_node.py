from prompts.outline_generator_prompt import OutlineGeneratorPrompt
from langchain_core.messages import SystemMessage, HumanMessage
from schemas.story_outline_schema import StoryOutline
import logging

logger = logging.getLogger(__name__)



class StoryOutlineNode:

    def __init__(self, llm):
        # Wrap the LLM with structured output to match StoryOutline schema
        self.llm = llm.with_structured_output(StoryOutline, method="json_mode")
        self.outline_generator_prompt = OutlineGeneratorPrompt()

    def story_outline_node(self, state):
        logger.info("Generating story outline...")
        """
        Generate a structured comic story outline and update the state.
        """
        # Invoke LLM with system prompt + user input
        response = self.llm.invoke([
            SystemMessage(content=self.outline_generator_prompt.system_prompt),
            HumanMessage(
                content=f"Generate a story outline using the following inputs:\n{state['user_input']}"
            )
        ])

        # Convert structured output to dictionaries for state
        story_phases = [phase.model_dump() for phase in response.story_phases]
        characters = [char.model_dump() for char in response.characters]
        logger.info(f"Story outline generated successfully generated number of phases: {len(story_phases)} and characters: {len(characters)}")
        # Return updated state
        return {
            "story_title": response.story_title,
            "story_overview": response.story_overview,
            "world_building": response.world_building,
            "story_phases": story_phases,
            "character": characters
        }