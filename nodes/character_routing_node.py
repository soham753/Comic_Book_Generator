
class InitCharacterNode:

    def run(self, state):
        return {
            "current_character_index": 0,
            "character_image_generation_prompt": state.get("character_image_generation_prompt", [])
        }

class CharacterSelectorNode:

    def run(self, state):

        index = state["current_character_index"]
        characters = state["character"]

        character = characters[index]

        return {
            "current_character": character
        }


class NextCharacterNode:

    def run(self, state):

        return {
            "current_character_index": state["current_character_index"] + 1
        }


def character_router(state):

    index = state["current_character_index"]
    total = len(state["character"])

    if index < total:
        return "next"
    else:
        return "end"
