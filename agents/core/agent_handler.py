from agents.config import GEMINI_API_KEY
from agents.core.epic_performer import EpicPerformer
from agents.core.instructions_handler import InstructionsHandler
from agents.core.llm_handler import GeminiHandler
from agents.db.service.epic_service import EpicService


class AgentHandler:

    def __init__(self):

        pass

    def execute_open_epics(self):

        epic_list = EpicService().find_open()
        epic_performer = EpicPerformer()

        for epic in epic_list:
            print(f"Performing epic:\n {epic.description}\n\n")
            epic_performer.perform(epic)

        print("All epics were performed.")

