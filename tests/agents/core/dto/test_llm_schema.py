import unittest

from agents.core.dto.llm_schema import FunctionSchema


class TestInstruction(unittest.TestCase):

    def test_instantiation(self):

        def function_for_tes(arg1: str):
            return arg1
        args = {
            "arg1": "This is a argument value!"
        }
        instructon_dict = {
            "function_name": function_for_tes,
            "arguments": args
        }


