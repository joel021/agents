from agents.constants import PROJECT_MANAGER_AGENT_NAME
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.dto.message_dto import MessageDTO
from agents.core.pm_agent.database_handler import DatabaseHandler
from agents.core.pm_agent.project_manager_agent import ProjectManagerAgent
from agents.db.service.epic_service import EpicService
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn


def start_project_manager_agent():

    redis_instance, pubsub = get_redis_conn()
    database_handler = DatabaseHandler(EpicService())
    pm_agent = ProjectManagerAgent(get_new_llm_reasoner(), database_handler, redis_instance)

    print("\nProject Manager agent started.")
    for message in pubsub.listen():

        message_dict = decode_message(message)
        if message_dict:
            pm_agent.reason(MessageDTO(**message_dict))

    print(f"{PROJECT_MANAGER_AGENT_NAME} stopped to listen.")

