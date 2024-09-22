from agents.core.instructions_handler import InstructionsHandler
from agents.core.llm_handler import LLMHandler
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.task import Task


class TaskPerformer:

    def __init__(self, llm_handler: LLMHandler, task_service: TaskService, story_service: StoryService):
        self.task_service = task_service
        self.story_service = story_service
        self.llm_handler = llm_handler
        self.instructions_handler = InstructionsHandler(task_service)

    def perform(self, task: Task, story_id: str, current_summary: str) -> Task:

        self.task_service.set_status(task, Status.IN_PROGRESS)
        prompt = (f"In story_id={story_id}. Given we have done: {current_summary}. Solve the following task: "
                   f"{task.description}. Break it down into more tasks, in new_tasks, If the task is too complex.")

        instructions_dict = self.llm_handler.generate_instructions_dict(prompt)
        self.task_service.set_summary(task, instructions_dict.get("summary", ""))
        self.story_service.create_tasks_to_story_id(story_id, instructions_dict.get("new_tasks", []))

        resp = self.instructions_handler.execute_instructions(instructions_dict.get("instructions", []))

        return task

