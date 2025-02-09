from agents.db.service.epic_service import EpicService
from agents.core.actuator.class_inspector import get_class_description


class DatabaseHandler:

    def __init__(self, epic_service: EpicService):

        self.epic_service = epic_service
        self.available_actions = get_class_description(EpicService, self.epic_service)

    def get_available_epic_actions(self) -> str:
        return str(self.available_actions).replace("'",
                                                                "\"").replace(" ", "")

