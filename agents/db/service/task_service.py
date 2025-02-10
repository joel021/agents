from agents.db.service.story_service import StoryService
from agents.db.status import Status
from agents.db.task import Task
from bson import ObjectId


class TaskService:

    def __init__(self, story_service: StoryService):
        self.story_service = story_service
    
    def get_by_id(self, task_id: str) -> Task:
        try:
            task = Task.objects.get(id=task_id)
            return task
        except Exception as e:
            print(f"Error retrieving task with id {task_id}: {e}")
            return None

    def set_status(self, task: Task, status: Status) -> dict:

        if isinstance(task, dict):
            task = Task.objects.get(id=task['id'])

        task.status = status
        return task.save().to_dict()

    def create(self, story_id: str, description: str) -> dict:

        task = Task(status=Status.TODO, description=description).save()
        self.story_service.add_task(story_id, task)
        return task.to_dict()

    def set_summary(self, task: Task, summary: str) -> dict:

        if isinstance(task, dict):
            task = Task.objects.get(id=task['id'])
        task.summary = summary
        return task.save().to_dict()

    def set_instructions(self, task: Task, instructions: list[dict]) -> dict:

        if isinstance(task, dict):
            task = Task.objects.get(id=task['id'])

        task.instructions = instructions
        return task.save()

    def find_by_id(self, id: str) -> dict:
        return Task.objects.get(id=id).to_dict()
