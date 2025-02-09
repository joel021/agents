import json

from redis import Redis

from agents.config import REDIS_CHANEL
from agents.constants import OPERATION_SYSTEM_AGENT_NAME
from agents.core.dto.llm_schema import ArgumentSchema, GenerateOSInstructionsSchema
from agents.core.dto.response import Response
from agents.core.llm_reasoner import LLMReasoner
from agents.core.message import Message
from agents.core.os_agent.instruction_performer import OsInstructions
from agents.utils.redis_utils import publish_message


class OperationSystemAgent:

    def __init__(self, llm: LLMReasoner, redis_instance: Redis):
        self.os_instructions = OsInstructions()
        self.llm = llm
        self.redis_instance = redis_instance

    def convert_to_dict(self, argument_responses: list[ArgumentSchema]) -> dict:
        args = {item['arg']: item['value'] for item in argument_responses}
        return {k: v for k, v in args.items() if v is not None}

    def send_message(self, recipient: str, message: str):

        message_str = json.dumps(Message(
            sender=OPERATION_SYSTEM_AGENT_NAME,
            recipient=recipient,
            message=message,
        ).to_dict())
        publish_message(self.redis_instance, REDIS_CHANEL, message_str)

    def reason(self, message: dict):

        if not message or not message.get('recipient', None) == OPERATION_SYSTEM_AGENT_NAME:
            return

        prompt = f"You are a Ubuntu specialist and you are in a group of your team. {message['sender']} have sent" \
        f"the following message: \n{message['message']}. Consider that you can perform the following actions: " \
        f"{self.os_instructions.get_available_instructions_str()}. If the request is not valid, answer setting" \
        f"```valid:False```. "

        instructions = self.llm.reason_dict(prompt, GenerateOSInstructionsSchema)

        answer = None
        if instructions.get('valid', False):
            answer = self.execute_instruction(instructions)

        if not answer:
            resp = (f"I could not attend to the message: {message['message']} ."
                    "because the request is invalid. I can only perform actions related to"
                     f"{self.os_instructions.get_available_instructions_str()}")
            self.send_message(message['sender'], resp)
        elif answer.error:
            resp = (f"I could not attend to the message: {message['message']} ."
                    f"due to {answer.msg}")
            self.send_message(message['sender'], resp)
        else:
            self.send_message(message['sender'], f"Request done: {message['message']}")

    def execute_instruction(self, instruction: dict) -> Response:

        function_name = instruction.get("function_name", None)
        if not function_name:
            return Response(f"Only use the provided set of possible instructions.", True)

        function_callable = self.os_instructions.actions.get(function_name, {}).get("function", None)
        if not function_callable:
            return Response(f"Unsupported instruction: {function_name}", True)

        args_dict = self.convert_to_dict(instruction.get("arguments", []))
        try:
            return function_callable(**args_dict)
        except Exception as e:
            return Response(f"Error executing instructions: {e}", True)

