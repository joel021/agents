from agents.config import GEMINI_API_KEY
from agents.core.llm_handler import GeminiHandler
from agents.core.performer.story_performer import StoryPerformer
from agents.db.epic import Epic
from agents.db.service.epic_service import EpicService
from agents.db.service.story_service import StoryService
from agents.db.status import Status
from agents.db.story import Story


class EpicPerformer:

    def __init__(self, epic_service: EpicService, story_service: StoryService):
        self.epic_service = epic_service
        self.story_service = story_service
        self.llm_handler = GeminiHandler(GEMINI_API_KEY)
        self.story_performer = StoryPerformer(self.llm_handler, self.story_service)

    def break_into_stories(self, epic: Epic) -> list[Story]:

        prompt_prefix = ('Software Engineering context. Answer in json format, nothing more, like this: '
                         '{"summary": "summarize what have done", "new_stories": [{"title": "story title 1",'
                         '"specification":"..."}, {"title": "story title 2", "specification": "..."}')
        prompt = (
            f"{prompt_prefix}Using scrum methodology for development. Break the following Epic into stories and put in "
            f"new_stories: {epic.description}.")

        resp_dict = self.llm_handler.generate_instructions_dict(prompt)
        self.epic_service.create_stories(epic, resp_dict.get("new_stories", []))
        return self.epic_service.set_summary(epic, resp_dict.get("summary", ""))

    def perform(self, epic: Epic) -> Epic:

        self.epic_service.set_status(epic, Status.IN_PROGRESS)

        if not epic.stories:
            epic = self.break_into_stories(epic)

        stories = list(epic.stories)
        i = 0
        summary = epic.summary
        while stories:

            story = self.story_performer.perform(stories[i], summary)
            if story.is_done():
                self.story_service.set_status(stories.pop(i), Status.DONE)

            if i == 0:
                summary = story.summary
            else:
                summary += story.summary

            i += 1

        return epic
