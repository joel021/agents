from redis import Redis

from agents.constants import PROJECT_MANAGER_AGENT_NAME, USER_NAME, AGENTS_DESCRIPTIONS
from agents.core.actuator.actions_performer import ActionsPerformer
from agents.core.dto.response import Response
from agents.core.llm_reasoner import LLMReasoner
from agents.core.dto.message_dto import MessageDTO
from agents.core.pm_agent.database_handler import DatabaseHandler
from agents.core.pm_agent.schemas import MessageAgents, GenerateDataBaseActionsSchema
from agents.core.actuator.redis_comm import publish_message


class ProjectManagerAgent:

    def __init__(self, llm_reasoner: LLMReasoner, database_handler: DatabaseHandler, redis_connection: Redis):
        self.llm_reasoner = llm_reasoner
        self.database_handler = database_handler
        self.redis_connection = redis_connection
        self.instructions_performer = ActionsPerformer(self.database_handler.available_actions)
        self.plan_summary = ""
        self.messages_summary = ""

    def _command_agents(self, command_result: dict):

        if command_result:
            for message_dict in command_result.get('messages', []):
                publish_message(self.redis_connection, message_dict)

    def _reason_agents(self, message: MessageDTO) -> dict:
        """Reasons about agent interactions and returns the reasoning dictionary."""

        prompt = (f"You have received a message from {message.sender}. You have to manage the agents and communicate "
                  f"to the user, if necessary.: \n"
                  f"{message.message}. "
                  f"The specification of the agents are: {AGENTS_DESCRIPTIONS}")

        return self.llm_reasoner.reason_dict(prompt, MessageAgents)

    def _reason_actions(self, message: MessageDTO, interaction_reasoning_dict: dict) -> dict:
        """Reasons about necessary actions and returns the reasoning dictionary."""

        prompt = (f"You have received a message from {message.sender}: \n"
                  f"{message.message}. Then, you commanded them as follows: \n {interaction_reasoning_dict}. "
                  f"Decide whether is necessary or not perform an action among the available: "
                  f"{self.database_handler.get_available_epic_actions()}. The project overview is: {self.plan_summary}."
                  f"The past messages resume is: {self.messages_summary}.")
        return self.llm_reasoner.reason_dict(prompt, GenerateDataBaseActionsSchema)

    def _execute_actions_and_generate_response(self, message: MessageDTO, actions_reasoning_dict: dict) -> str:
        """Executes actions and generates a response message."""

        results, result = self.instructions_performer.execute_actions(actions_reasoning_dict.get('actions', []))

        if isinstance(result, Response):
            if result.error:
                return (
                    f"Could not attend to '{message.message}'. I have encountered the following problem: "
                    f"{result.msg}")
            else:
                return f"I have finished doing: {actions_reasoning_dict.get('summary', '')}."
        else:
            return self.llm_reasoner.simple_answer(f"Write a concise text summarizing the following "
                                                   f"set of actions in text flow: {results}")

    def reason(self, message: MessageDTO) -> bool:
        """Handles message reasoning, action execution, and response sending."""

        if message.recipient != PROJECT_MANAGER_AGENT_NAME and message.sender != USER_NAME:
            return False

        interaction_reasoning_dict = self._reason_agents(message)
        self._command_agents(interaction_reasoning_dict)

        actions_reasoning_dict = self._reason_actions(message, interaction_reasoning_dict)
        msg_str = self._execute_actions_and_generate_response(message, actions_reasoning_dict)

        answer_dict = MessageDTO(sender=PROJECT_MANAGER_AGENT_NAME, recipient=message.sender,
                              message=msg_str).to_dict()
        publish_message(self.redis_connection, answer_dict)
        self.update_memory(message.to_dict(), answer_dict, actions_reasoning_dict.get("summary", ""))
        return True

    def update_memory(self, message: dict, agent_answer: dict, summary: str):

        messages = str([message, agent_answer])
        self.messages_summary = self.llm_reasoner.simple_answer(f"Summary the following messages: {messages}")
        self.plan_summary += summary

