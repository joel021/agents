import os
import unittest

from agents.config import WORK_DIR
from agents.constants import PROJECT_MANAGER_AGENT_NAME, OPERATION_SYSTEM_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.message import Message
from agents.core.os_agent.operation_system_agent import OperationSystemAgent
from agents.utils.redis_utils import get_redis_conn


class TestOperationSystemAgent(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.makedirs(f"{WORK_DIR}/test", exist_ok=True)

    def test_reason_create_file(self):

        redis_instance, pubsub = get_redis_conn()
        os_system_agent = OperationSystemAgent(get_new_llm_reasoner(), redis_instance)

        message = Message(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=OPERATION_SYSTEM_AGENT_NAME,
            message=f"Create or replace a file, at {WORK_DIR}/test/new_file.py with the following contents:"
                    f"print('Hello World!')",
            data=None
        )
        performed = os_system_agent.reason(message.to_dict())

        assert performed, "Performed without errors."

