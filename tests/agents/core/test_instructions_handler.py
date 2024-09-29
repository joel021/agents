import unittest

from agents.core.dto.llm_schema import ArgumentSchema
from agents.core.instructions_handler import InstructionsHandler


class TestGeminiHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_convert_to_dict(self):
        instruction_handler = InstructionsHandler()

        args = [ArgumentSchema(arg="arg1", value="value"),
                ArgumentSchema(arg="arg2", value="value"),
                ArgumentSchema(arg="arg3", value="value")]
        args_dict = instruction_handler.convert_to_dict(args)

        assert args_dict['arg1']

    def test_execute_instruction(self):

        instruction_handler = InstructionsHandler()
        instructions = {
                "function_name": "execute_terminal",
                "arguments": [
                    {
                        "arg": "path",
                        "value": "/home/joel/"
                    },
                    {
                        "arg": "command",
                        "value": "ls"
                    }
                ]
            }

        response = instruction_handler.execute_instruction(instructions)
        assert not response.error
