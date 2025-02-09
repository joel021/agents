import unittest

import mongomock
from mongoengine import disconnect, connect

from agents.core.agents_switch import AgentSwitch
from agents.core.os_agent.instructions_performer import InstructionsPerformer
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.story import Story
from agents.db.task import Task
from agents.config import WORK_DIR, SINGLE_AGENTS


class TestTaskPerformer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

        self.agents_switch = AgentSwitch(SINGLE_AGENTS)
        story_service = StoryService()
        self.story = Story(title="Restaurant CRUD.").save()
        self.task_performer = InstructionsPerformer(self.agents_switch, TaskService(story_service), story_service)

    def test_perform(self):
        specification = (
            "Create the User model implementation for authentication. User has name, address, birthdate, email. "
            "We are using Python 3, poetry, and mongoengine."
            f"The project location will be at {WORK_DIR}/. So, create the project, "
            f"including creating the restaurant folder."
        )
        task = Task(title="Title",
                    specification=specification)

        performed_task = self.task_performer.perform(task, str(self.story.id),
                                                     "Nothing done yet")
        assert performed_task.status == Status.DONE
