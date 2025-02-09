import unittest

from agents.constants import PROJECT_MANAGER_AGENT_NAME, RESEARCH_AGENT_NAME
from agents.core.actuator.redis_comm import get_redis_conn
from agents.core.dto.message_dto import MessageDTO
from agents.core.research_agent.research_agent import ResearchAgent
from agents.utils.redis_utils import get_redis_conn

class TestResearchAgent(unittest.TestCase):


    def test_reason_search_query(self):

        redis_instance, pubsub = get_redis_conn()
        research_agent = ResearchAgent(redis_instance)

        message = MessageDTO(
            sender=PROJECT_MANAGER_AGENT_NAME,
            recipient=RESEARCH_AGENT_NAME,
            message="What is artificial intelligence?",
            data=None
        )
        print("Message being sent to reason:", message.to_dict())
        
        performed = research_agent.reason(message.to_dict())
        print("Message being sent to reason:", performed)

        assert performed, "Performed without errors."

