from agents.config import GEMINI_API_KEY
from agents.core.llm_handler import GeminiHandler
from agents.core.story_performer import StoryPerformer
from agents.db.epic import Epic
from agents.db.service.epic_service import EpicService
from agents.db.service.story_service import StoryService
from agents.db.status import Status
from agents.db.story import Story


class EpicPerformer:

    def __init__(self, epic_service: EpicService, story_service: StoryService):
        self.epic_service = epic_service
        self.story_service = story_service

        prompt_prefix = ("""Software Engineering context. Answer in json format, nothing more, like this: {"instructions": [{"function": "function_name",
                "args":{"arg1":"v1","arg2":"v2"}},...], "summary": "summarize the instructions", "new_tasks": 
        ["Any required task, described here in normal text."], "new_stories":...}. """)

        prompt_suffix = (""" Possible instructions: {"function":"execute_command_line", 
                "args":{"command": "(str)"}}.""")
        self.llm_handler = GeminiHandler(GEMINI_API_KEY,
                                         prompt_prefix,
                                         prompt_suffix)
        self.story_performer = StoryPerformer(self.llm_handler, self.story_service)

    def break_into_stories(self, epic: Epic) -> list[Story]:
        resp_dict = self.llm_handler.generate_instructions_dict("Using scrum methodology for "
                                                                   "development. "
                                                                   "Break the following Epic into stories and put in "
                                                                   "new_stories: "
                                                                   f"{epic.description}")
        new_stories = resp_dict.get("new_stories", [])
        return self.epic_service.create_stories(epic, new_stories)

    def perform(self, epic: Epic) -> Epic:

        self.epic_service.set_status(epic, Status.IN_PROGRESS)
        stories = epic.stories
        i = 0
        if not stories:
            stories = self.break_into_stories(epic)

        while stories:

            story = self.story_performer.perform(stories[i])
            if story.is_done():
                self.story_service.set_status(stories.pop(i), Status.DONE)

            i += 1

        return epic
