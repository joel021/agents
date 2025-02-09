from agents.core.llm_reasoner import LLMReasoner
from agents.core.pm_agent.epic_performer import EpicPerformer
from agents.db.service.epic_service import EpicService
from agents.db.service.story_service import StoryService
from agents.db.status import Status


class ProjectManagerAgent:

    def __init__(self, epic_service: EpicService, llm_reasoner: LLMReasoner):
        self.llm_reasoner = llm_reasoner
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
