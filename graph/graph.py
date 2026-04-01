from langgraph.graph import StateGraph, START, END
from state.state import ComicState
from nodes.story_outline_node import StoryOutlineNode
from nodes.panel_generator_node import PanelGeneratorNode
from nodes.routing_phase_nodes import InitPhaseNode, PhaseSelectorNode, NextPhaseNode, phase_router
from nodes.dialogue_generator_node import DialogueGeneratorNode
from nodes.character_image_genration_promt_generator_node import CharacterImageGenerationPromptGeneratorNode
from nodes.character_routing_node import InitCharacterNode, CharacterSelectorNode, NextCharacterNode, character_router
from  nodes.comic_page_image_generation_promt_node import ComicPageImageGenerationPromptNode


class ComicGraph:
    def __init__(self, llm):
        self.llm = llm



        self.story_outline_node = StoryOutlineNode(llm)
        self.graph_builder = StateGraph(ComicState)
        self.init_phase_node = InitPhaseNode()
        self.phase_selector_node = PhaseSelectorNode()
        self.panel_generator_node = PanelGeneratorNode(llm)
        self.dialogue_generator_node = DialogueGeneratorNode(llm)
        self.next_phase_node = NextPhaseNode()
        self.init_character_node = InitCharacterNode()
        self.character_selector_node = CharacterSelectorNode()
        self.next_character_node = NextCharacterNode()
        self.character_image_generation_prompt_generator_node = CharacterImageGenerationPromptGeneratorNode(llm)
        self.comic_page_image_generation_prompt_node = ComicPageImageGenerationPromptNode(llm)








        self.graph_builder.add_node("story_outline_node", self.story_outline_node.story_outline_node)
        self.graph_builder.add_node("init_phase_node", self.init_phase_node.run)
        self.graph_builder.add_node("phase_selector_node", self.phase_selector_node.run)
        self.graph_builder.add_node("panel_generator_node", self.panel_generator_node.panel_generator_node)
        self.graph_builder.add_node("dialogue_generator_node", self.dialogue_generator_node.run)
        self.graph_builder.add_node("comic_page_image_generation_prompt_node", self.comic_page_image_generation_prompt_node.run)
        self.graph_builder.add_node("next_phase_node", self.next_phase_node.run)
        self.graph_builder.add_node("init_character_node", self.init_character_node.run)
        self.graph_builder.add_node("character_selector_node", self.character_selector_node.run)
        self.graph_builder.add_node("character_image_generation_prompt_generator_node", self.character_image_generation_prompt_generator_node.character_image_generation_prompt_generator_node)
        self.graph_builder.add_node("next_character_node", self.next_character_node.run)







        self.graph_builder.add_edge(START, "story_outline_node")
        self.graph_builder.add_edge("story_outline_node", "init_phase_node")
        self.graph_builder.add_edge("init_phase_node", "phase_selector_node")
        self.graph_builder.add_edge("phase_selector_node", "panel_generator_node")
        self.graph_builder.add_edge("panel_generator_node", "dialogue_generator_node")
        self.graph_builder.add_edge("dialogue_generator_node", "comic_page_image_generation_prompt_node")
        self.graph_builder.add_edge("comic_page_image_generation_prompt_node", "next_phase_node")

        self.graph_builder.add_conditional_edges(
            "next_phase_node",
            phase_router,
            {
                "next": "phase_selector_node",
                "end": "init_character_node"
            }
        )
        self.graph_builder.add_edge("init_character_node", "character_selector_node")
        self.graph_builder.add_edge("character_selector_node", "character_image_generation_prompt_generator_node")
        self.graph_builder.add_edge("character_image_generation_prompt_generator_node", "next_character_node")
        self.graph_builder.add_conditional_edges(
            "next_character_node",
            character_router,
            {
                "next": "character_selector_node",
                "end": END
            }
        )