from agents.core.dto.response import Response
from agents.logger import logger
from agents.core.actuator.class_inspector import execute_function


class ActionsPerformer:

    def __init__(self, actions: dict):
        self.actions = actions

    def execute_actions(self, actions: list[dict]) -> (list, Response):
        """
        Execute instructions dynamically, updating the instruction set after each one based on feedback from the LLM.
        """
        results = []
        current_result = None
        performed_instructions = []

        if not actions:
            return Response("No actions to perform", False)

        while actions:
            action = actions.pop(0)
            current_result = self._execute_single_instruction(action, results, performed_instructions)

            if current_result.error:
                logger.error(current_result.msg)
                break

        return results, current_result

    def _execute_single_instruction(self, action: dict, results: list[dict], performed_instructions: list[dict]) -> Response:
        """Execute a single instruction and log the result."""
        current_result = execute_function(action, self.actions)
        results.append({
            "action": action,
            "result": current_result
        })

        print(f"Executing action: {action}\n result: {current_result}")

        if not current_result.error:
            performed_instructions.append(action)

        return current_result
