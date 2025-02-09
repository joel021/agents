from unittest.mock import patch
import unittest
from agents.db.redis_connection import get_redis_conn
from agents.message_dto import MessageDTO
from agents.constants import PROJECT_MANAGER_AGENT_NAME, SOFTWARE_ENGINEER_AGENT_NAME
from agents.software_engineer_agent import SoftwareEngineer

class TestSoftwareEngineerAgent(unittest.TestCase):

    def test_reason_task_resolution(self):
        redis_instance, pubsub = get_redis_conn()
        software_engineer_agent = SoftwareEngineer(redis_instance)

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=SOFTWARE_ENGINEER_AGENT_NAME,
            message="60b8d6d6b0e4a45f12345678",  # A MongoDB task ID as a string.
            data=None
        )
        print("Message being sent to reason:", message.to_dict())
        performed = software_engineer_agent.reason(message.to_dict())

        assert performed, "Performed without errors."

if __name__ == '__main__':
    unittest.main()
