import unittest

from agents.core.dto.llm_schema import ArgumentSchema
from agents.core.llm_reasoner import get_new_llm_reasoner
from agents.core.actuator.action_performer import ActionsPerformer
from agents.core.os_agent.os_instructions import OsInstructions


class TestInstructionPerformer(unittest.TestCase):


    def test_convert_to_dict(self):

        instructions_performer = ActionsPerformer(get_new_llm_reasoner(), OsInstructions())

        args = [ArgumentSchema(arg="arg1", value="value"),
                ArgumentSchema(arg="arg2", value="value"),
                ArgumentSchema(arg="arg3", value="value")]
        args_dict = instructions_performer.convert_to_dict(args)

        assert args_dict['arg1']

    def test_execute_instruction(self):

        instructions_performer = ActionsPerformer(get_new_llm_reasoner(), OsInstructions())
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

        response = instructions_performer.execute_instruction(instructions)
        assert not response.error
