from agents.db.status import Status
from agents.db.story import Story
from agents.db.task import Task


class StoryService:

    def __init__(self):
        pass

    def create_tasks_to_story_id(self, story_id: str, tasks: list[Task]) -> list[Task] | None:
        story = Story.objects(id=story_id).first()

        if not story:
            return None

        return self.create_tasks(story, tasks)

    def create_tasks(self, story: Story, tasks: list[Task]) -> list[Task]:

        if story.tasks is None:
            story.tasks = []

        for task in tasks:
            story.tasks.append(task.save())

        story.save()
        return tasks

    def set_status(self, story: Story, status: Status):
        story.status = status
        return story.save()

    def add_task(self, story_id: str, task: Task) -> Story | None:

        story = Story.objects(id=story_id).first()

        if not story:
            return None

        if story.tasks is None:
            story.tasks = []

        story.tasks.append(task)
        return story.save()

