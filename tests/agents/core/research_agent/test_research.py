import os
import unittest

from agents.config import WORK_DIR
from agents.constants import PROJECT_MANAGER_AGENT_NAME, RESEARCH_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.message import Message
from agents.core.research_agent.research_agent import ResearchAgent
from agents.utils.redis_utils import get_redis_conn
from unittest.mock import patch

class TestResearchAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(f"{WORK_DIR}/test", exist_ok=True)

    @patch("agents.utils.web.search_web")
    def test_reason_search_query(self,mock_search_web):

        mock_search_web.return_value = [
        {"title": "Artificial Intelligence", "snippet": "AI is the simulation of human intelligence..."}
        ]

        redis_instance, pubsub = get_redis_conn()
        research_agent = ResearchAgent(get_new_llm_reasoner(), redis_instance)

        message = Message(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=RESEARCH_AGENT_NAME,
            message="What is artificial intelligence?",
            data=None
        )
        print("Message being sent to reason:", message.to_dict())
        performed = research_agent.reason(message.to_dict())

        assert performed, "Performed without errors."

