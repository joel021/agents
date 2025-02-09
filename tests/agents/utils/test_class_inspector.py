import unittest

from agents.core.actuator.class_inspector import get_class_description, execute_function


class ClassToBeTested:

    def __init__(self, class_name: str):
        self.class_name = class_name

    def sum(self, a: int, b: int) -> int:

        return a + b

    def return_name(self):
        return self.class_name


class TestActions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_retrieve_sum_method(self):

        class_to_be_tested_instance = ClassToBeTested("Name")
        dict_class = get_class_description(ClassToBeTested, class_to_be_tested_instance)
        a, b, expected_sum = 1, 2, 3

        assert dict_class['sum']['function'](a, b) == expected_sum

    def test_retrieve_return_name_method(self):

        name = "Name"
        class_to_be_tested_instance = ClassToBeTested(name)
        dict_class = get_class_description(ClassToBeTested, class_to_be_tested_instance)

        assert dict_class['return_name']['function']() == name

    def test_execute_action_sum(self):

        name = "Name"
        class_to_be_tested_instance = ClassToBeTested(name)
        available_functions = get_class_description(ClassToBeTested, class_to_be_tested_instance)

        action_dict = {
            "function_name": "sum",
            "arguments": [
                {"arg": "a", "value": 1},
                {"arg": "b", "value": 2},
            ]
        }
        result = execute_function(action_dict, available_functions)
        assert result == 3
