from langchain_core.messages import SystemMessage, HumanMessage
from prompts.panel_generator_prompt import PanelGeneratorPrompt
from schemas.panael_generator_schema import PanelOutline
import logging

logger = logging.getLogger(__name__)




class PanelGeneratorNode:

    def __init__(self, llm):
        self.llm = llm.with_structured_output(
            PanelOutline,
            method="json_mode"
        )
        self.panel_generator_prompt = PanelGeneratorPrompt()

    def panel_generator_node(self, state):
        logger.info(f"Generating panels for number of phase: {state['current_phase_index'] + 1}")

        phase = state["current_phase"]

        response = self.llm.invoke([
            SystemMessage(content=self.panel_generator_prompt.system_prompt),
            HumanMessage(
                content=f"""
Generate comic panels for this phase.

Title: {phase['phase_title']}
Description: {phase['description']}
Characters: {phase['characters']}
"""
            )
        ])

        panels = [panel.model_dump() for panel in response.panels]
        logger.info(f"Panels generated successfully for phase: {state['current_phase_index'] + 1} and number of panels: {len(panels)}")

        return {
            "panels": panels
        }

