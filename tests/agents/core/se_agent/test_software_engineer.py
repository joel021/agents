from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.db.service.task_service import TaskService
from agents.db.task import Task
import mongomock
import unittest

from mongoengine import connect, disconnect

from agents.core.actuator.redis_comm import get_redis_conn
from agents.core.dto.message_dto import MessageDTO
from agents.constants import PROJECT_MANAGER_AGENT_NAME, SOFTWARE_ENGINEER_AGENT_NAME
from agents.core.software_engineer.softwate_engineer_agent import SoftwareEngineer


class TestSoftwareEngineerAgent(unittest.TestCase):

    @classmethod
    def setUp(self):
        disconnect()
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
        self.task = Task(title='Criar uma função de soma').save()


    def test_reason_task_resolution(self):
        redis_instance, pubsub = get_redis_conn()
        software_engineer_agent = SoftwareEngineer(redis_instance, get_new_llm_reasoner(), TaskService())

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=SOFTWARE_ENGINEER_AGENT_NAME,
            message="Please, resolve the task id 60b8d6d6b0e4a45f12345678",  # A MongoDB task ID as a string.
            data=self.task.to_dict()
        )
        print("Message being sent to reason:", message.to_dict())
        performed = software_engineer_agent.reason(message.to_dict())

        assert performed, "Performed without errors."

    def test_reason_task_without_data(self):
        redis_instance, pubsub = get_redis_conn()
        software_engineer_agent = SoftwareEngineer(redis_instance, get_new_llm_reasoner(), TaskService())

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=SOFTWARE_ENGINEER_AGENT_NAME,
            message="Please resolve the task id 60b8d6d6b0e4a45f12345678",
            data=None
        )
        print("Message being sent to reason:", message.to_dict())
        performed = software_engineer_agent.reason(message.to_dict())

        assert not performed, "Not perform no exceptions."
