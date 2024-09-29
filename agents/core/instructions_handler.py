from agents.core.dto.llm_schema import ArgumentSchema
from agents.core.performer.instruction_performer import InstructionPerformer
from agents.core.dto.response import Response


class InstructionsHandler:

    def __init__(self):
        self.performer = InstructionPerformer()

    def convert_to_dict(self, argument_responses: list[ArgumentSchema]) -> dict:
        args = {item['arg']: item['value'] for item in argument_responses}
        return {k: v for k, v in args.items() if v is not None}

    def execute_instruction(self, instruction: dict) -> Response:

        function_name = instruction.get("function_name", None)
        if not function_name:
            return Response(f"Only use the provided set of possible instructions.", True)

        function_callable = self.performer.actions.get(function_name, {}).get("function", None)
        if not function_callable:
            return Response(f"Unsupported instruction: {function_name}", True)

        args_dict = self.convert_to_dict(instruction.get("arguments", []))
        print(args_dict)
        try:
            return function_callable(**args_dict)
        except Exception as e:
            return Response(f"Error executing instructions: {e}", True)


