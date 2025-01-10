import unittest

from agents.config import WORK_DIR
from agents.utils.files import recursive_scan


class TestActions(unittest.TestCase):

    def test_scan_directory(self):

        folder_structure = recursive_scan(WORK_DIR)
        assert folder_structure


