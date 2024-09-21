from agents.core.actions import Actions
from agents.core.response import Response


class InstructionsHandler:

    def __init__(self):

        self.actions = Actions()

    def execute_instructions(self, instructions: dict):

        action = instructions.get("action", None)
        if not action:
            return Response(None, False)

        action_method = self.actions.actions.get(action, None)
        if not action_method:
            return Response(f"Unsupported action: {action}", True)

        expected_args = instructions.get("args", {})
        args = {k: v for k, v in expected_args.items() if v is not None}

        try:
            return action_method(**args)
        except Exception as e:
            return Response(f"Error executing instructions: {e}", True)

