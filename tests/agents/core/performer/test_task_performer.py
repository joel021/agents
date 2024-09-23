import unittest

import mongomock
from mongoengine import disconnect, connect

from agents.core.llm_handler import GeminiHandler
from agents.config import GEMINI_API_KEY
from agents.core.performer.task_performer import TaskPerformer
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.task import Task


class TestTaskPerformer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

        self.gemini_handler = GeminiHandler(GEMINI_API_KEY)
        story_service = StoryService()
        self.task_performer = TaskPerformer(self.gemini_handler, TaskService(story_service), story_service)
        self.task = Task(title="Title",
                    specification="Create a service Java class on package com.restaurant for create User. "
                                  "User has name and email. The project location is /home/joel/documents/restaurant/.").save()
    def test_perform_system(self):

        task = Task(title="Title",
                    specification="Create a service Java class on package com.restaurant for create User. "
                                  "User has name and email. The project location is /home/joel/documents/restaurant/.")

        performed_task = self.task_performer.perform(task, "story_001",
                                                     "We have created the project, it is empty yet.")
        print(performed_task.summary)
        assert performed_task.status == Status.DONE

    def test_execute_task_resp_unit(self):

        prompt = ("Create a service Java class on package com.restaurant for create User. "
                    "User has name and email. The project location is /home/joel/documents/restaurant/.")
        resp, task = self.task_performer.execute_task(self.task, prompt, "story_001")
        assert not resp.error

    def test_execute_task_task_unit(self):
        prompt = ("Create a service Java class on package com.restaurant for create User. "
                  "User has name and email. The project location is /home/joel/documents/restaurant/.")
        resp, task = self.task_performer.execute_task(self.task, prompt, "story_001")
        assert task.summary

    def test_try_solve_unit(self):

        resp, task = self.task_performer.try_solve(self.task,
                                      "We have created the project, it is empty yet.",
                                      "story_001",
                                      "We have created the project, it is empty yet.")
        assert not resp.error

    def test_try_solve_unit(self):

        resp, task = self.task_performer.try_solve(self.task,
                                      "We have created the project, it is empty yet.",
                                      "story_001",
                                      "We have created the project, it is empty yet.")
        assert not resp.error

