import unittest

import mongomock
from mongoengine import disconnect, connect

from agents.core.actuator.actions_performer import ActionsPerformer
from agents.core.pm_agent.database_handler import DatabaseHandler
from agents.db.epic import Epic
from agents.db.service.epic_service import EpicService
from agents.db.status import Status


class TestActionsPerformer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        self.epic = Epic(title="Tile", status=Status.IN_PROGRESS, description="description").save()

    def test_save_epic(self):

        database_handler = DatabaseHandler(EpicService())

        epic_dict = {
            "title": "Epic created by action performer",
            "status": Status.TODO,
            "description": "Do something.",
        }
        actions = [
            {
                "function_name": "create",
                "arguments": [
                    {
                        "arg": "epic",
                        "value": epic_dict
                    }
                ]
            }
        ]
        actions_performer = ActionsPerformer(database_handler.available_actions)
        last, results = actions_performer.execute_actions(actions)

        assert len(results) > 0, "Executed the requested actions, which is save an epic in the database successfully."

    def test_add_stories(self):

        database_handler = DatabaseHandler(EpicService())

        story_dict = {
            "title": "Epic created by action performer",
            "status": Status.TODO,
            "description": "Do something.",
        }
        actions = [
            {
                "function_name": "add_stories",
                "arguments": [
                    {
                        "arg": "epic",
                        "value": self.epic.to_dict()
                    },
                    {
                        "arg": "stories",
                        "value": [story_dict]
                    }
                ]
            }
        ]
        actions_performer = ActionsPerformer(database_handler.available_actions)
        last, results = actions_performer.execute_actions(actions)

        assert len(results) > 0, "Added a story into a existing epic in the database successfully."


    def test_find_by_status(self):

        database_handler = DatabaseHandler(EpicService())

        actions = [
            {
                "function_name": "find_by_status",
                "arguments": [
                    {
                        "arg": "status",
                        "value": str(self.epic.status.name)
                    }
                ]
            }
        ]
        actions_performer = ActionsPerformer(database_handler.available_actions)
        last, results = actions_performer.execute_actions(actions)
        assert len(results) > 0, "Found by status."

    def test_set_status(self):

        database_handler = DatabaseHandler(EpicService())

        actions = [
            {
                "function_name": "set_status",
                "arguments": [
                    {
                        "arg": "status",
                        "value": Status.DONE
                    },
                    {
                        "arg": "epic",
                        "value": self.epic.to_dict()
                    }
                ]
            }
        ]
        actions_performer = ActionsPerformer(database_handler.available_actions)
        last, results = actions_performer.execute_actions(actions)

        assert last[0]['result'].to_dict().get('status') == Status.DONE.name
