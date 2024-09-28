from agents.utils.files import scan_project, create_file, update_file, read_file
from agents.utils.system_os import execute_terminal


class InstructionPerformer:

    def __init__(self):
        self.actions = {

            "execute_terminal": {
                "function": execute_terminal,
                "args": {
                    "path": "(str) required",
                    "command": "(str) any Ubuntu 22.04 command or commands"
                }
            },
            "scan_project_folders_files": {
                "function": scan_project,
                "args": {
                    "path": "(str) root or specific part of the project complete path",
                }
            },
            "create_file": {
                "function": create_file,
                "args": {
                    "file_path": "(str) file path",
                    "content": "(str) file content",
                }
            },
            "update_file": {
                "function": update_file,
                "args": {
                    "file_path": "(str) file path",
                    "content": "(str) file content",
                }
            },
            "read_file": {
                "function": read_file,
                "args": {
                    "file_path": "(str) file path",
                }
            }
        }

    @staticmethod
    def get_available_instructions_str():
        return str(InstructionPerformer().actions).replace("'", "\"").replace(" ", "")
