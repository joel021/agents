from agents.constants import RESEARCH_AGENT_NAME

from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.research_agent.research_agent import ResearchAgent
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn


def start_researcher_agent():

    redis_instance, pubsub = get_redis_conn()
    research_handler = ResearchAgent(get_new_llm_reasoner(), redis_instance)

    print("Researcher agent started.")

    for message in pubsub.listen():

        message_dict = decode_message(message)
        research_handler.reason(message_dict)

    print(f"{RESEARCH_AGENT_NAME} stopped to listen.")

