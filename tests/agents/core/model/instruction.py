import unittest

from agents.core.model.instruction import Instruction


class TestInstruction(unittest.TestCase):

    def test_instantiation(self):

        def function_for_tes(arg1: str):
            return arg1
        args = {
            "arg1": "This is a argument value!"
        }
        instructon_dict = {
            "function": function_for_tes,
            "args": args,
            "summary": "This is the summary!",
            "next_tasks": [{"function": function_for_tes}]
        }

        instruction = Instruction(**instructon_dict)
        assert instruction
