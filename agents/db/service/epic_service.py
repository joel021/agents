from agents.db.epic import Epic
from agents.db.status import Status
from agents.db.story import Story


class EpicService:

    def find_by_status(self, status: Status):

        if isinstance(status, str):
            status = Status.from_keyword(status)

        return Epic.objects(status=status)

    def create(self, epic: dict) -> Epic:

        return Epic.from_dict(epic).save()

    def add_stories(self, epic: Epic, stories: list[Story]) -> list[Story]:

        if isinstance(epic, dict):
            epic = self.find_by_id(epic.get("id"))

        if epic.stories is None:
            epic.stories = []

        for story in stories:
            if isinstance(story, dict):
                story = Story.from_dict(story)
            epic.stories.append(story.save())

        epic.save()
        return epic.stories

    def set_status(self, epic: Epic, status: Status):

        if isinstance(epic, dict):
            epic = self.find_by_id(epic.get("id"))

        epic.status = status
        return epic.save()

    def set_summary(self, epic: Epic, summary: str):

        if isinstance(epic, dict):
            epic = self.find_by_id(epic.get("id"))

        epic.summary = summary
        return epic.save()

    def find_by_id(self, id: str) -> Epic:
        return Epic.objects.get(id=id)

    def delete(self, id: str):

        Epic.objects.get(id=id).delete()
