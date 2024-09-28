import unittest

from agents.core.dto.response import Response
from agents.utils.system_os import execute_terminal


class TestSystemOs(unittest.TestCase):


    def test_execute_terminal_error(self):

        response: Response = execute_terminal('~', 'invalid_command')
        assert response.error

    def test_execute_terminal_direct_test(self):

        response: Response = execute_terminal('~', 'ls')

        assert not response.msg is None
        assert not response.error
