from redis import Redis

from agents.constants import OPERATION_SYSTEM_AGENT_NAME
from agents.core.dto.llm_schema import GenerateOSActionsSchema
from agents.core.dto.response import Response
from agents.core.llm_reasoner import LLMReasoner
from agents.core.dto.message_dto import MessageDTO
from agents.core.actuator.actions_performer import ActionsPerformer
from agents.core.os_agent.os_instructions import OsInstructions
from agents.core.actuator.redis_comm import publish_message


class OperationSystemAgent:

    def __init__(self, llm: LLMReasoner, redis_instance: Redis):
        self.os_instructions = OsInstructions()
        self.llm = llm
        self.redis_instance = redis_instance
        self.instructions_performer = ActionsPerformer(self.os_instructions.actions)

    def send_message(self, recipient: str, message: str):

        message_dict = MessageDTO(
            sender=OPERATION_SYSTEM_AGENT_NAME,
            recipient=recipient,
            message=message,
        ).to_dict()
        publish_message(self.redis_instance, message_dict)

    def reason(self, message: dict) -> bool:

        if not message or not message.get('recipient', None) == OPERATION_SYSTEM_AGENT_NAME:
            return False

        prompt = (f"You are a Ubuntu specialist and you are in a group of your team. {message['sender']} have sent"
                  f"the following message: \n{message['message']}. Consider that you can perform the following actions: "
                  f"{self.os_instructions.get_available_instructions_str()}. If the request is not valid, answer setting"
                  f"```valid:False```. Whenever need to install things directly to Ubuntu system, configure and run the "
                  f"docker-compose.yml instead.")

        llm_answer = self.llm.reason_dict(prompt, GenerateOSActionsSchema)
        instructions = llm_answer.get('instructions', [])

        last_result = None
        if llm_answer.get('valid', False):
            results, last_result = self.instructions_performer.execute_actions(instructions)

        if not last_result:
            resp = (f"I could not attend to the message: {message['message']} ."
                    "because the request is invalid. I can only perform actions related to"
                     f"{self.os_instructions.get_available_instructions_str()}")
            self.send_message(message['sender'], resp)
            return False
        elif isinstance(last_result, Response) and last_result.error:
            resp = (f"I could not attend to the message: {message['message']} ."
                    f"due to {last_result.msg}")
            self.send_message(message['sender'], resp)
            return False
        else:
            self.send_message(message['sender'], f"Request done: {message['message']}. "
                                                 f"The result is: \n{last_result}")
            return True
