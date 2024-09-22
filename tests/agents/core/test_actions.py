import unittest
from agents.core.instruction_performer import InstructionPerformer
from agents.core.model.response import Response


class TestActions(unittest.TestCase):

    def test_execute_terminal_error(self):

        response: Response = InstructionPerformer().execute_terminal('~', 'invalid_command')
        assert response.error

    def test_execute_terminal_direct_test(self):

        response: Response = InstructionPerformer().execute_terminal('~', 'ls')

        assert not response.msg is None
        assert not response.error

    def test_action_from_dict(self):

        args = {"path": '~', "command": 'ls'}
        result: Response = InstructionPerformer().actions.get("execute_terminal").get("instruction")(**args)
        assert not result.error

