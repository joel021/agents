from agents.core.performer.instruction_performer import InstructionPerformer
from agents.core.model.instruction import Instruction
from agents.core.model.response import Response
from agents.db.service.task_service import TaskService


class InstructionsHandler:

    def __init__(self, task_service: TaskService):
        self.performer = InstructionPerformer(task_service)

    def execute_instruction(self, instruction: Instruction):

        if not instruction.function_name:
            return Response(None, False)

        function_callable = self.performer.actions.get(instruction.function_name, None)
        if not function_callable:
            return Response(f"Unsupported action: {instruction.function_name}", True)

        args = {k: v for k, v in instruction.args.items() if v is not None}

        try:
            return function_callable(**args)
        except Exception as e:
            return Response(f"Error executing instructions: {e}", True)

    def execute_instructions(self, instructions: list[dict]):

        for instruction in instructions:
            response = self.execute_instruction(Instruction(**instruction))

            if response.error:
                return response

        return Response(None, False)
