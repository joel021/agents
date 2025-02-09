from agents.constants import RESEARCH_AGENT_NAME

from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.research_agent.research_agent import ResearchAgent
from agents.utils.jsons import decode_message
from agents.utils.redis_utils import get_redis_conn


def start_os_agent():

    redis_instance, pubsub = get_redis_conn(RESEARCH_AGENT_NAME)
    os_instruction_handler = ResearchAgent(get_new_llm_reasoner(), redis_instance)

    for message in pubsub.listen():

        message_dict = decode_message(message)
        os_instruction_handler.reason(message_dict)

    print(f"{RESEARCH_AGENT_NAME} stopped to listen.")