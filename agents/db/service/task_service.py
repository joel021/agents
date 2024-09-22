from agents.db.service.story_service import StoryService
from agents.db.status import Status
from agents.db.task import Task


class TaskService:

    def __init__(self, story_service: StoryService):
        self.story_service = story_service

    def set_status(self, task: Task, status: Status) -> Task:

        task.status = status
        return task.save()

    def create(self, story_id: str, description: str) -> Task:

        task = Task(status=Status.TODO, description=description).save()
        self.story_service.add_task(story_id, task)
        return task

    def set_summary(self, task: Task, summary: str) -> Task:

        task.summary = summary
        return task.save()

