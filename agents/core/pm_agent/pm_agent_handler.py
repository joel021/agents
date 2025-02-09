from agents.constants import PROJECT_MANAGER_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.message import Message
from agents.core.pm_agent.project_manager_agent import ProjectManagerAgent
from agents.db.service.epic_service import EpicService
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn


def start_os_agent():

    redis_instance, pubsub = get_redis_conn()

    pm_agent = ProjectManagerAgent(get_new_llm_reasoner(), EpicService())

    for message in pubsub.listen():

        message_dict = decode_message(message)
        pm_agent.reason(Message(**message_dict))

    print(f"{PROJECT_MANAGER_AGENT_NAME} stopped to listen.")

