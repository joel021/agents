import unittest

from agents.core.dto.llm_reponse import ArgumentResponse
from agents.core.instructions_handler import InstructionsHandler


class TestGeminiHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_convert_to_dict(self):
        instruction_handler = InstructionsHandler()

        args = [ArgumentResponse(arg="arg1", value="value"),
                ArgumentResponse(arg="arg2", value="value"),
                ArgumentResponse(arg="arg3", value="value")]
        args_dict = instruction_handler.convert_to_dict(args)

        assert args_dict['arg1']



