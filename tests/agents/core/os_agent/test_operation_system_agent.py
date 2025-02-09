import os
import unittest

from agents.config import WORK_DIR
from agents.constants import PROJECT_MANAGER_AGENT_NAME, OPERATION_SYSTEM_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.dto.message_dto import MessageDTO
from agents.core.os_agent.operation_system_agent import OperationSystemAgent
from agents.core.actuator.redis_comm import get_redis_conn


class TestOperationSystemAgent(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.makedirs(f"{WORK_DIR}/test", exist_ok=True)

    @classmethod
    def tearDownClass(self):
        os.remove(f"{WORK_DIR}/test/new_file.py")

    def test_reason_create_file(self):

        redis_instance, pubsub = get_redis_conn()
        os_system_agent = OperationSystemAgent(get_new_llm_reasoner(), redis_instance)

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=OPERATION_SYSTEM_AGENT_NAME,
            message=f"Create or replace a file, at {WORK_DIR}/test/new_file.py with the following contents:"
                    f"print('Hello World!')",
            data=None
        )
        performed = os_system_agent.reason(message.to_dict())

        assert performed, "Performed without errors."

