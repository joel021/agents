from agents.core.agents_switch import AgentSwitch
from agents.core.os_agent.instructions_performer import InstructionsPerformer
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.story import Story
from agents.logger import logger


class StoryPerformer:

    def __init__(self, agent_switch: AgentSwitch, story_service: StoryService):
        self.gemini_handler = agent_switch.get_llm_agent()
        self.story_service = story_service
        self.task_service = TaskService(story_service)
        self.task_performer = InstructionsPerformer(agent_switch, self.task_service, story_service)

    def breakdown_into_tasks(self, story: Story) -> Story:

        prompt = ('You are a software engineer. Answer in the following format: ```{"summary": "summarize the what '
                  'have done", "new_tasks": [{"title": "...", "specification": "..."}, ...]}```. Thinking about scrum '
                  f'methodology, break down the following Story into tasks and put in new_stories: {story.description}')

        resp_dict = self.gemini_handler.reason_dict(prompt)
        new_tasks = resp_dict.get("new_tasks", [])
        self.story_service.create_tasks(story, new_tasks)
        return self.story_service.set_summary(story, resp_dict.get("summary", ""))

    def summarize_actions(self, summary: str) -> str:

        prompt = ('Answer in the following format: ```{"summary": "text summarization without break line"}```. '
                  f'Summarize the following text: `{summary}`')
        return self.gemini_handler.reason_dict(prompt).get("summary", summary)

    def perform(self, story: Story, summary: str) -> Story:

        logger.info(f'Performing: {story.description}')

        self.story_service.set_status(story, Status.IN_PROGRESS)
        if not story.tasks:
            story = self.breakdown_into_tasks(story)

        tasks = list(story.tasks)
        summary = summary + story.summary

        i = 0
        while tasks:

            task = self.task_performer.perform(tasks[i], str(story.id), summary)

            if i == 0:
                summary = task.summary
            else:
                summary = self.summarize_actions(summary + task.summary)

            if task.is_done():
                self.task_service.set_status(tasks.pop(i), Status.DONE)

            i += 1

        return story
