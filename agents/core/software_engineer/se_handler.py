from agents.constants import SOFTWARE_ENGINEER_AGENT_NAME

from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.software_engineer.main import SoftwareEngineer
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn


def start_os_agent():

    print("Os Agent Started")
    redis_instance, pubsub = get_redis_conn()
    os_instruction_handler = SoftwareEngineer(get_new_llm_reasoner(), redis_instance)

    for message in pubsub.listen():

        message_dict = decode_message(message)
        os_instruction_handler.reason(message_dict)

    print(f"{OPERATION_SYSTEM_AGENT_NAME} stopped to listen.")