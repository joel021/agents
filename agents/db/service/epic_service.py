from agents.db.epic import Epic
from agents.db.status import Status
from agents.db.story import Story


class EpicService:

    def find_by_status(self, status: Status):
        return Epic.objects(status=status)

    def find_open(self) -> list[Epic]:

        epic_list = self.find_by_status(Status.IN_PROGRESS)

        if not epic_list:
            epic_list = Epic.objects(status=Status.TODO)

        return epic_list

    def create_stories(self, epic: Epic, stories: list[Story]) -> list[Story]:

        if epic.stories is None:
            epic.stories = []

        for story in stories:
            epic.stories.append(story.save())

        epic.save()
        return stories

    def set_status(self, epic: Epic, status: Status):

        epic.status = status
        return epic.save()

    def set_summary(self, epic: Epic, summary: str):
        epic.summary = summary
        return epic.save()
