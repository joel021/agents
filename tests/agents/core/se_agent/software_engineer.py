from agents.db.service.task_service import TaskService
from agents.db.task import Task
import mongomock
import unittest
from unittest.mock import patch

from mongoengine import connect, disconnect

from agents.db.epic import Epic
from agents.db.service.epic_service import EpicService
from agents.db.status import Status
from agents.db.story import Story

from agents.core.actuator.redis_comm import get_redis_conn
from agents.core.dto.message_dto import MessageDTO
from agents.constants import PROJECT_MANAGER_AGENT_NAME, SOFTWARE_ENGINEER_NAME
from agents.core.software_engineer.main import SoftwareEngineer



class TestSoftwareEngineerAgent(unittest.TestCase):

    @classmethod
    def setUp(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        self.task = Task(title='Criar uma função de soma').save()


    def test_reason_task_resolution(self):
        redis_instance, pubsub = get_redis_conn()
        task_service = TaskService()
        software_engineer_agent = SoftwareEngineer(redis_instance, task_service)

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=SOFTWARE_ENGINEER_NAME,
            message="60b8d6d6b0e4a45f12345678",  # A MongoDB task ID as a string.
            data=self.task.to_dict()
        )
        print("Message being sent to reason:", message.to_dict())
        performed = software_engineer_agent.reason(message.to_dict())

        assert performed, "Performed without errors."

if __name__ == '__main__':
    unittest.main()
