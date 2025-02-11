from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.software_engineer.softwate_engineer_agent import SoftwareEngineer
from agents.db.service.task_service import TaskService
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn


def start_software_engineer_agent():

    print("Software Engineer Agent Started")
    redis_instance, pubsub = get_redis_conn()
    task_service = TaskService()
    se_handler = SoftwareEngineer(redis_instance, get_new_llm_reasoner(), task_service)

    for message in pubsub.listen():

        message_dict = decode_message(message)
        se_handler.reason(message_dict)

    print(f"{SOFTWARE_ENGINEER_AGENT_NAME} stopped to listen.")