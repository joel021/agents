from agents.db.data_model import entity_list_to_dict_list
from agents.db.epic import Epic
from agents.db.status import Status
from agents.db.story import Story


class EpicService:


    def find_by_status(self, status: Status) -> list[dict]:

        if isinstance(status, str):
            status = Status.from_keyword(status)

        return entity_list_to_dict_list(Epic.objects(status=status))

    def create(self, epic: dict) -> dict:

        return Epic.from_dict(epic).save().to_dict()

    def add_stories(self, epic: Epic, stories: list[Story]) -> list[dict]:

        if isinstance(epic, dict):
            epic = Epic.objects.get(id=epic.get("id"))

        if epic.stories is None:
            epic.stories = []

        for story in stories:
            if isinstance(story, dict):
                story = Story.from_dict(story)
            epic.stories.append(story.save())

        epic.save()
        return epic.to_dict().get("stories")

    def set_status(self, epic: Epic, status: Status) -> dict:

        if isinstance(epic, dict):
            epic = Epic.objects.get(id=epic.get("id"))

        epic.status = status
        return epic.save().to_dict()

    def set_summary(self, epic: Epic, summary: str) -> dict:

        if isinstance(epic, dict):
            epic = Epic.objects.get(id=epic.get("id"))

        epic.summary = summary
        return epic.save().to_dict()

    def find_by_id(self, id: str) -> dict:
        return Epic.objects.get(id=id).to_dict()

    def delete(self, id: str):

        Epic.objects.get(id=id).delete()
