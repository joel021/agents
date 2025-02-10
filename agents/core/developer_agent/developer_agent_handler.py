from agents.constants import DEVELOPER_SPECIALIST_AGENT_NAME

from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.developer_agent.developer_specialist_agent import DeveloperSpecialistAgent
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn


def start_developer_specialist_agent():

    print("Developer Specialist Agent Started")
    redis_instance, pubsub = get_redis_conn()
    developer_handler = DeveloperSpecialistAgent(get_new_llm_reasoner(), redis_instance)

    for message in pubsub.listen():

        message_dict = decode_message(message)
        developer_handler.reason(message_dict)

    print(f"{DEVELOPER_SPECIALIST_AGENT_NAME} stopped to listen.")