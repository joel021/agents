import unittest

import mongomock
from mongoengine import disconnect, connect

from agents.core.llm_handler import GeminiHandler
from agents.config import GEMINI_API_KEY
from agents.core.performer.task_performer import TaskPerformer
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.story import Story
from agents.db.task import Task
from agents.config import WORK_DIR

class TestTaskPerformer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

        self.gemini_handler = GeminiHandler(GEMINI_API_KEY)
        story_service = StoryService()
        self.story = Story(title="Restaurant CRUD.").save()
        self.task_performer = TaskPerformer(self.gemini_handler, TaskService(story_service), story_service)
        specification = ("Create a service Java class on package com.restaurant for create User. "
                        f"User has name and email. The project location will be at {WORK_DIR}/restaurant.")

        self.task = Task(title="Create Restaurant CRUD project",
                        specification=specification
                        ).save()

    def test_perform(self):
        specification = (
            "Create the User model implementation for authentication. User has name, address, birthdate, email. "
            "The project package "
            "is com.auth.gourmet.Restaurant. We are using maven and Java 17 with Spring boot 3."
            f"The project location will be at {WORK_DIR}/restaurant. So, create the project and implement it."
        )
        task = Task(title="Title",
                    specification=specification)

        performed_task = self.task_performer.perform(task, str(self.story.id),
                                                     "We have created the project, it is empty yet. "
                                                     "We added the Spring Web dependency.")
        print(performed_task.instructions)

        assert performed_task.status == Status.DONE
