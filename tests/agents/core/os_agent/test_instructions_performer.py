import unittest

from agents.core.actuator.actions_performer import ActionsPerformer
from agents.core.os_agent.os_instructions import OsInstructions


class TestInstructionPerformer(unittest.TestCase):


    def test_execute_instruction(self):

        instructions_performer = ActionsPerformer(OsInstructions().actions)
        instructions = [{
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
            }]

        results, last = instructions_performer.execute_actions(instructions)
        assert len(results) > 0

