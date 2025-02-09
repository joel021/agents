from agents.constants import PROJECT_MANAGER_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.utils.jsons import decode_message
from agents.utils.redis_utils import get_redis_conn


def start_os_agent():

    redis_instance, pubsub = get_redis_conn(PROJECT_MANAGER_AGENT_NAME)
    pm_agent = ProjectManagerAgent(get_new_llm_reasoner(), redis_instance)

    for message in pubsub.listen():

        message_dict = decode_message(message)
        pm_agent.reason(message_dict)

    print(f"{PROJECT_MANAGER_AGENT_NAME} stopped to listen.")

