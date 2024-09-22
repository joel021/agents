from agents.core.llm_handler import GeminiHandler, LLMHandler
from agents.core.task_performer import TaskPerformer
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.story import Story
from agents.db.task import Task


class StoryPerformer:

    def __init__(self, llm_handler: LLMHandler, story_service: StoryService):
        self.gemini_handler = llm_handler
        self.story_service = story_service
        self.task_service = TaskService()
        self.task_performer = TaskPerformer(llm_handler, self.task_service)

    def breakdown_into_tasks(self, story: Story) -> list[Task]:

        resp_dict = self.gemini_handler.generate_instructions_dict("Thinking about scrum methodology for "
                                                                   "development. "
                                                                   "Break the following Story into tasks and put in "
                                                                   "new_stories: "
                                                                   f"{story.description}")
        new_tasks = resp_dict.get("new_tasks", [])
        return self.story_service.create_tasks(story, new_tasks)

    def perform(self, story: Story) -> Story:

        self.story_service.set_status(story, Status.IN_PROGRESS)
        tasks = story.tasks

        if not tasks:
            tasks = self.breakdown_into_tasks(story)

        i = 0
        while tasks:

            task = self.task_performer.perform(tasks[i])

            if task.is_done():
                self.task_service.set_status(tasks.pop(i), Status.DONE)

            i += 1

        return story
