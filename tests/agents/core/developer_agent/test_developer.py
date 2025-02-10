import os
import unittest

from agents.config import WORK_DIR
from agents.constants import PROJECT_MANAGER_AGENT_NAME, DEVELOPER_SPECIALIST_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.dto.message_dto import MessageDTO
from agents.core.developer_agent.developer_specialist_agent import DeveloperSpecialistAgent
from agents.core.actuator.redis_comm import get_redis_conn


class TestDeveloperSpecialist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.makedirs(f"{WORK_DIR}/test", exist_ok=True)

    @classmethod
    def tearDownClass(self):
        file_path = f"{WORK_DIR}/test/generated_artifact.py"
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_reason_generate_artifact(self):

        redis_instance, pubsub = get_redis_conn()
        developer_specialist_agent = DeveloperSpecialistAgent(get_new_llm_reasoner(), redis_instance)

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=DEVELOPER_SPECIALIST_AGENT_NAME,
            message="Develop a Python module that prints 'Hello, DeveloperAgent!'.",
            data=None
        )
        print("Message being sent to reason:", message.to_dict())

        performed = developer_specialist_agent.reason(message.to_dict())
        print("performed:", performed)

        self.assertTrue(performed, "The DeveloperAgent should successfully generate the software artifact.")