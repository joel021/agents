from redis import Redis
from agents.core.actuator.redis_comm import publish_message
from agents.core.dto.message_dto import MessageDTO
from agents.constants import SOFTWARE_ENGINEER_AGENT_NAME, DEVELOPER_SPECIALIST_AGENT_NAME
from agents.core.llm_reasoner import LLMReasoner
from agents.core.software_engineer.inputs_prompts import create_prompts_prompt


class SoftwareEngineer:

    def __init__(self, redis_instance: Redis, llm_reasoner: LLMReasoner, task_service):
        self.task_service = task_service
        self.redis_instance = redis_instance
        self.llm_reasoner = llm_reasoner

    def send_message(self, recipient: str, message: str):

        message_dict = MessageDTO(
            sender=SOFTWARE_ENGINEER_AGENT_NAME,
            recipient=recipient,
            message=message,
        ).to_dict()
        publish_message(self.redis_instance, message_dict)

    def create_prompts(self, task):
        se_prompt = create_prompts_prompt(task)
        text = self.llm_reasoner.simple_answer(se_prompt)
        return text
    
    def reason(self, message: dict) -> bool:
        if not message or not message.get('recipient', None) == SOFTWARE_ENGINEER_AGENT_NAME:
            return False
        
        data = message.get('data', None)
        task_id = data.get('id', None) if data else None
        task = self.task_service.get_by_id(task_id) if task_id else None

        prompt = self.create_prompts(task)

        if prompt:
            self.send_message(DEVELOPER_SPECIALIST_AGENT_NAME, prompt)
            return True
        else:
            resp = (
                f"I could not attend to the message: {message['message']}."
            )
            self.send_message(message['sender'], resp)
            return False
    
