import unittest
from agents.actions import Actions
from agents.response import Response


class TestActions(unittest.TestCase):

    def test_execute_terminal_error(self):

        response: Response = Actions().execute_terminal('~', 'invalid_command')
        assert response.error

    def test_execute_terminal_direct_test(self):

        response: Response = Actions().execute_terminal('~', 'ls')

        assert not response.msg is None
        assert not response.error

    def test_action_from_dict(self):

        args = {"path": '~', "command": 'ls'}
        result: Response = Actions().actions.get("execute_terminal").get("instruction")(**args)
        assert not result.error

