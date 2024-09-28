import subprocess
import os

from agents.core.dto.response import Response
from agents.db.service.task_service import TaskService
from agents.utils.files import recursive_scan


class InstructionPerformer:

    def __init__(self, task_service: TaskService):
        self.task_service = task_service
        self.actions = {

            "execute_terminal": {
                "function": self.execute_terminal,
                "args": {
                    "path": "(str) required",
                    "command": "(str) any Ubuntu 22.04 command or commands"
                }
            },
            "scan_project_folders_files": {
                "function": self.scan_project,
                "args": {
                    "path": "(str) root or specific part of the project complete path",
                }
            },
            "create_file": {
                "function": self.create_file,
                "args": {
                    "file_path": "(str) file path",
                    "content": "(str) file content",
                }
            },
            "update_file": {
                "function": self.update_file,
                "args": {
                    "file_path": "(str) file path",
                    "content": "(str) file content",
                }
            },
            "read_file": {
                "function": self.read_file,
                "args": {
                    "file_path": "(str) file path",
                }
            }
        }

    def execute_terminal(self, path: str, command: str):
        path = os.path.expanduser(path)
        process = subprocess.Popen(command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        result = stdout.decode('utf-8')
        if stderr:
            error = stderr.decode('utf-8')
            return Response(error, True)

        return Response(result, False)

    def create_file(self, file_path: str):
        return Response("created successfully.", error=False)

    def update_file(self, file_path: str, content: str):
        return Response("updated successfully.", error=False)

    def scan_project(self, path: str, content: str):
        return recursive_scan(path)

    def read_file(self, path: str):
        return Response("reading successfully.", error=False)

    @staticmethod
    def get_available_instructions_str():
        return str(InstructionPerformer(None).actions).replace("'", "\"").replace(" ", "")
