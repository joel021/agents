import unittest

import mongomock
from mongoengine import connect, disconnect

from agents.db.epic import Epic
from agents.db.service.epic_service import EpicService
from agents.db.status import Status
from agents.db.story import Story


class TestDeviceChat(unittest.TestCase):

    @classmethod
    def setUp(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        self.epic_service = EpicService()

    def test_find_open_todo(self):

        self.todo_epic = Epic(
            status=Status.TODO,
            description="Epic description",
            stories=None).save()

        epic_list = self.epic_service.find_open()
        assert len(epic_list) == 1

    def test_find_open_progress(self):
        self.todo_epic = Epic(
            status=Status.IN_PROGRESS,
            description="Epic description",
            stories=None).save()

        epic_list = self.epic_service.find_open()
        assert len(epic_list) == 1

    def test_find_open_done(self):
        self.todo_epic = Epic(
            status=Status.DONE,
            description="Epic description",
            stories=None).save()

        epic_list = self.epic_service.find_open()
        assert len(epic_list) == 0

    def test_create_stories(self):
        epic = Epic(
            status=Status.DONE,
            description="Epic description",
            stories=None).save()
        stories = [Story(description="Story1"), Story(description="Story2")]
        stories_saved = self.epic_service.add_stories(epic, stories)

        assert len(stories_saved) == 2
