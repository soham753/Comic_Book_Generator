
class InitPhaseNode:

    def run(self, state):
        return {
            "current_phase_index": 0,
            "comic_pages": state.get("comic_pages", [])
        }

class PhaseSelectorNode:

    def run(self, state):

        index = state["current_phase_index"]
        phases = state["story_phases"]

        phase = phases[index]

        return {
            "current_phase": phase
        }


class NextPhaseNode:

    def run(self, state):

        return {
            "current_phase_index": state["current_phase_index"] + 1
        }


def phase_router(state):

    index = state["current_phase_index"]
    total = len(state["story_phases"])

    if index < total:
        return "next"
    else:
        return "end"
