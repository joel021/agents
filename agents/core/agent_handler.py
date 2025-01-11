from agents.core.agents_switch import AgentSwitch
from agents.core.performer.epic_performer import EpicPerformer
from agents.db.service.epic_service import EpicService
from agents.db.service.story_service import StoryService
from agents.db.status import Status


class AgentHandler:

    def __init__(self, epic_service: EpicService, agent_switch: AgentSwitch):
        self.agent_switch = agent_switch
        self.story_service = StoryService()
        self.epic_service = epic_service

    async def execute_open_epics(self):

        epic_performer = EpicPerformer(self.agent_switch, self.epic_service, self.story_service)

        progress_epic_list = self.epic_service.find_by_status(Status.IN_PROGRESS)

        for epic in progress_epic_list:
            print(f"Performing epic:\n {epic.description}\n\n")
            epic_performer.perform(epic)

        todo_epic_list = self.epic_service.find_by_status(Status.TODO)
        for epic in todo_epic_list:
            print(f"Performing epic:\n {epic.description}\n\n")
            epic_performer.perform(epic)

        print("Finished.")
