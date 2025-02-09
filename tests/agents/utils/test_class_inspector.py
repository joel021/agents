import unittest

from agents.utils.class_inspector import get_class_description

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
