import os
import unittest

from agents.config import WORK_DIR
from agents.utils.files import recursive_scan


class TestActions(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        if not os.path.exists(WORK_DIR):
            os.makedirs(WORK_DIR, exist_ok=True)

    def test_scan_directory(self):

        folder_structure = recursive_scan(WORK_DIR)
        assert folder_structure
