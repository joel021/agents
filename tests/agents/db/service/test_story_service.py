import unittest

import mongomock
from mongoengine import connect, disconnect

from agents.db.service.story_service import StoryService
from agents.db.story import Story
from agents.db.task import Task


class TestStoryService(unittest.TestCase):

    @classmethod
    def setUp(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        self.story_service = StoryService()
        self.story = Story().save()

    def test_add_task(self):

        story_id = str(self.story.id)
        task = Task(specification="Description of task").save()
        story = self.story_service.add_task(story_id, task)

        assert len(story.tasks) > 0
