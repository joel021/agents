from redis import Redis

from agents.constants import DEVELOPER_SPECIALIST_AGENT_NAME
from agents.core.dto.response import Response
from agents.core.llm_reasoner import LLMReasoner
from agents.core.dto.message_dto import MessageDTO
from agents.core.actuator.artifact_generator import ArtifactGenerator
from agents.core.developer_agent.schemas import GenerateSoftwareArtifactsSchema
from agents.core.actuator.redis_comm import publish_message


class DeveloperSpecialistAgent:

    def __init__(self, llm: LLMReasoner, redis_instance: Redis):
        self.llm = llm
        self.redis_instance = redis_instance
        self.artifact_generator = ArtifactGenerator()

    def send_message(self, recipient: str, message: str):

        message_dict = MessageDTO(
            sender=DEVELOPER_SPECIALIST_AGENT_NAME,
            recipient=recipient,
            message=message,
        ).to_dict()
        publish_message(self.redis_instance, message_dict)

    def reason(self, message: dict) -> bool:
        if not message or not message.get('recipient', None) == DEVELOPER_SPECIALIST_AGENT_NAME:
            return False

        prompt = (f"You are a software development specialist. {message['sender']} has provided the following "
                  f"specifications: \n{message['message']}. Your task is to develop the requested software artifact, "
                  f"ensuring quality and compliance with the requirements. If the request is invalid, respond setting "
                  f"```valid:False```. ")

        llm_answer = self.llm.reason_dict(prompt, GenerateSoftwareArtifactsSchema)
        artifact_code = llm_answer.get('artifact_code', '')

        if not llm_answer.get('valid', False) or not artifact_code:
            resp = (f"I could not fulfill the request: {message['message']} . "
                    "The request is either invalid or lacks sufficient details for implementation.")
            self.send_message(message['sender'], resp)
            return False
        
        result = self.artifact_generator.generate(artifact_code)
        
        if isinstance(result, Response) and result.error:
            resp = (f"I encountered an error while developing the software artifact: {message['message']} . "
                    f"Error details: {result.msg}")
            self.send_message(message['sender'], resp)
            return False
        else:
            self.send_message(message['sender'], f"Software artifact successfully developed based on specifications.\n"
                                                 f"Generated Code:\n{artifact_code}")
            return True
