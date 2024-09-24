import unittest

from agents.utils.files import recursive_scan
from agents.utils.jsons import extract_json


class TestJsons(unittest.TestCase):

    def test_extract_json(self):

        text = ('```json '
                '{"instructions": [{"function_name": "execute_terminal", "args": {"path": "/home/joel/documents/'
                'restaurant", "command": "mkdir -p com/restaurant"}}, {"function_name": "create_task", "args": '
                '{"epic_id": "story_001", "specification": "Create a Java class named User.java in the package '
                'com/restaurant, with fields for name and email."}}, {"function_name": "create_task", "args": '
                '{"epic_id": "story_001", "specification": "Create a constructor for the User class to initialize '
                'the name and email fields."}}, {"function_name": "create_task", "args": {"epic_id": "story_001", '
                '"specification": "Create a getter method for the name field in the User class."}}, {"function_name": '
                '"create_task", "args": {"epic_id": "story_001", "specification": "Create a getter method for the email'
                'field in the User class."}}], "summary": "Create a new directory for the package com/restaurant, then '
                'create a Java class named User.java in that directory. The class should have fields for name and email'
                ', a constructor to initialize these fields, and getter methods for both fields.", "new_tasks": []}'
                '```')

        result_dict = extract_json(text)
        assert result_dict['instructions']

