import json
import os.path
import unittest

from agents.core.dto.llm_schema import BreakEpicIntoStoriesSchema, BreakStoryIntoTasksSchema, StorySchema, \
    GenerateOSActionsSchema
from agents.core.llm_reasoner import GeminiReasoner
from agents.config import GEMINI_API_KEY, WORK_DIR
from agents.core.pm_agent.instruction_performer import InstructionPerformer


class TestGeminiHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.gemini_handler = GeminiReasoner(GEMINI_API_KEY)
        self.gemini_handler_2 = GeminiReasoner(GEMINI_API_KEY)

        print(f"aattempting to create: {WORK_DIR}")
        os.makedirs(WORK_DIR, exist_ok=True)

    def test_generate_instructions_break_into_stories(self):
        prompt = ("Create a web server REST API for authentication."
                  " The functional requirements are: login (email and receive expirable link),"
                  " logout. The non functional requirements are: authentication by JWT token, use relational database'"
                  "for persistence. The architecture decision are: java 23, spring boot 3, postgress sql,"
                  "junit tests for each method, junit for system tests. The project was just created on folder"
                  " ~/gemini/"
                  "auth_spring/ with package name as com.auth.gourmet.restaurant. "
                  "You have any permissions to do whatever in this folder, create, delete, update, read, "
                  "etc. To any files as well.")
        response_text = self.gemini_handler.reason(prompt, BreakEpicIntoStoriesSchema)
        assert json.loads(response_text)

    def test_generate_instructions_break_into_tasks(self):
        prompt = ("Create the service module for CRUD of User."
                  "The package name is com.example.restaurant. The project location is /home/gemini/restaurant/ ."
                  "The project was just created using spring boot 3 initializer. Break this story into specific "
                  "well specified tasks for guide the developers develop this feature.")
        response_text = self.gemini_handler.reason(prompt, BreakStoryIntoTasksSchema)
        assert json.loads(response_text)

    def test_create_tasks(self):

        prompt = "Create Spring Boot project."
        response_text = self.gemini_handler.reason(prompt, list[StorySchema])
        assert json.loads(response_text)

    def test_generate_instructions_dict(self):
        prompt = ('Create UserController: Create a new Spring Boot controller in the package '
                  '`com.example.restaurant.controller` named `UserController`. The project location is '
                  '/home/joel/gemini/restaurant and the package name is com.restaurant. Consider User is on '
                  'model package in com.example.restaurant.model.User and has the following attributes: '
                  'name, email, password, roles. The available actions for perform this task are: '
                  f'{InstructionPerformer.get_available_instructions_str()}')
        response_dict = self.gemini_handler.reason_dict(prompt, GenerateOSActionsSchema)
        assert response_dict
