from agents.core.dto.llm_schema import ArgumentSchema
from agents.core.llm_reasoner import LLMReasoner
from agents.core.dto.response import Response
from agents.core.os_agent.os_instructions import OsInstructions
from agents.logger import logger


class InstructionsPerformer:

    def __init__(self, reasoner: LLMReasoner, os_instructions: OsInstructions):
        self.os_instructions = os_instructions
        self.reasoner = reasoner

    def execute_instructions(self, instructions: list) -> Response:
        """
        Execute instructions dynamically, updating the instruction set after each one based on feedback from the LLM.
        """
        results = []
        current_result = None
        performed_instructions = []

        if not instructions:
            return Response("No instructions to execute", False)

        while instructions:
            instruction = instructions.pop(0)
            current_result = self._execute_single_instruction(instruction, results, performed_instructions)

            if current_result.error:
                logger.error(current_result.msg)
                break

        return current_result

    def _execute_single_instruction(self, instruction, results, performed_instructions) -> Response:
        """Execute a single instruction and log the result."""
        current_result = self.execute_instruction(instruction)
        results.append({
            "instruction": instruction,
            "result": current_result
        })

        print(f"Executing instruction: {instruction}\n result: {current_result}")

        if not current_result.error:
            performed_instructions.append(instruction)

        return current_result

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

    def convert_to_dict(self, argument_responses: list[ArgumentSchema]) -> dict:
        args = {item['arg']: item['value'] for item in argument_responses}
        return {k: v for k, v in args.items() if v is not None}

