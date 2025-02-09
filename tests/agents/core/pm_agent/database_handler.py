import unittest

import mongomock
from mongoengine import disconnect, connect

from agents.core.pm_agent.database_handler import DatabaseHandler
from agents.db.service.epic_service import EpicService


class TestDatabaseHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

    def test_get_available_actions(self):

        database_handler = DatabaseHandler(EpicService())

        assert len(database_handler.get_available_epic_actions()) > 0

