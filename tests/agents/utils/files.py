import unittest

from agents.utils.files import recursive_scan


class TestActions(unittest.TestCase):

    def test_scan_directory(self):

        folder_structure = recursive_scan("/home/joel/Documents/Restaurant/src")
        assert folder_structure


