import unittest
from agents.core.performer.instruction_performer import InstructionPerformer
from agents.core.dto.response import Response


class TestInstructionPerformer(unittest.TestCase):


    def test_action_from_dict(self):

        args = {"path": '~', "command": 'ls'}
        result: Response = InstructionPerformer().actions.get("execute_terminal").get("function")(**args)
        assert not result.error

