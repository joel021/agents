from agents.core.agents_switch import AgentSwitch
from agents.core.performer.epic_performer import EpicPerformer
from agents.db.service.epic_service import EpicService
from agents.db.service.story_service import StoryService


class AgentHandler:

    def __init__(self, agent_switch: AgentSwitch):
        self.agent_switch = agent_switch
        self.epic_service = EpicService()
        self.story_service = StoryService()

    def execute_open_epics(self):

        epic_list = self.epic_service.find_open()
        epic_performer = EpicPerformer(self.agent_switch, self.epic_service, self.story_service)

        for epic in epic_list:
            print(f"Performing epic:\n {epic.description}\n\n")
            epic_performer.perform(epic)

        print("All epics were performed.")

