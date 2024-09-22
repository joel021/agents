import unittest

from agents.core.llm_handler import GeminiHandler
from agents.config import GEMINI_API_KEY


class TestGeminiHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        prompt_prefix = ("""Answer in json format, nothing more, like this: {"instructions": [{"function": "function_name",
"args":{"arg1":"v1","arg2":"v2"}},...], "text": "summarize the instructions", "next_tasks": 
["Any required task, described here in normal text."]}""")

        prompt_suffix = ("""Possible actions: {"function":"execute_command_line", 
"args":{"command": "(str)"}}. If the task is too big, break it down in sub tasks, on "next_tasks" instead and let 
instructions empty.""")
        self.gemini_handler = GeminiHandler(GEMINI_API_KEY,
                                            prompt_prefix,
                                            prompt_suffix)
        self.gemini_handler_2 = GeminiHandler(GEMINI_API_KEY, "","")

    def test_generate_instructions(self):
        prompt = ("Create a web server REST API for authentication."
                  " The functional requirements are: login (email and receive expirable link),"
                  " logout. The non functional requirements are: authentication by JWT token, use relational database'"
                  "for persistence. The architecture decision are: java 23, spring boot 3, postgress sql,"
                  "junit tests for each method, junit for system tests. The project was just created on folder ~/gemini/"
                  "auth_spring/ with package name as com.auth.gourmet.restaurant.You have any permissions to do whatever in this folder, create, delete, update, read, "
                  "etc. To any files as well.")
        response_text = self.gemini_handler.generate_instructions(prompt)
        assert response_text

    def test_create_tasks(self):

        prompt = "Create Spring Boot project."
        response_text = self.gemini_handler.generate_instructions(prompt)
        assert response_text

    def test_two_sections(self):
        answer = self.gemini_handler_2.generate_instructions("Summary what I have asked to you until now.")
        assert answer

    def test_generate_instructions_dict(self):
        prompt = ("Create a web server REST API for authentication."
                  " The functional requirements are: login (email and receive expirable link),"
                  " logout. The non functional requirements are: authentication by JWT token, use relational database'"
                  "for persistence. The architecture decision are: java 23, spring boot 3, postgress sql,"
                  "junit tests for each method, junit for system tests. The project was just created on folder ~/gemini/"
                  "auth_spring/ with package name as com.auth.gourmet.restaurant.You have any permissions to do whatever in this folder, create, delete, update, read, "
                  "etc. To any files as well.")
        response_dict = self.gemini_handler.generate_instructions_dict(prompt)
        assert response_dict
