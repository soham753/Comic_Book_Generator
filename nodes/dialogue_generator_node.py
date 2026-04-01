from langchain_core.messages import SystemMessage, HumanMessage
from prompts.dialogue_generator_prompt import DialogueGeneratorPrompt
from schemas.dialogue_generator_schema import DialogueOutline
import logging

logger = logging.getLogger(__name__)



class DialogueGeneratorNode:

    def __init__(self, llm):

        self.llm = llm.with_structured_output(
            DialogueOutline,
            method="json_mode"
        )

        self.prompt = DialogueGeneratorPrompt()

    def run(self, state):
        logger.info(f"Generating dialogue for number of phase: {state['current_phase_index'] + 1}")

        phase = state["current_phase"]
        panels = state["panels"]

        response = self.llm.invoke([
            SystemMessage(content=self.prompt.system_prompt),
            HumanMessage(
                content=f"""
Write dialogue for the following comic panels.

Phase:
{phase}

Panels:
{panels}
"""
            )
        ])

        dialogue_panels = [p.model_dump() for p in response.panels]

        # merge dialogue into panels
        updated_panels = []

        for panel in panels:

            dialogue_data = next(
                (d for d in dialogue_panels if d["panel_number"] == panel["panel_number"]),
                None
            )

            if dialogue_data:
                panel["dialogue"] = dialogue_data["dialogue"]
                panel["caption"] = dialogue_data.get("caption")

            updated_panels.append(panel)
        logger.info(f"Dialogue generated successfully for phase: {state['current_phase_index'] + 1} ")
        return {
            "panels": updated_panels
        }