import subprocess
import os

from agents.core.model.response import Response
from agents.db.service.task_service import TaskService


class InstructionPerformer:

    def __init__(self, task_service: TaskService):

        self.task_service = task_service
        self.actions = {

            "execute_terminal": {
                "function": self.execute_terminal,
                "args": {
                    "path": "str required",
                    "command": "str required"
                }
            },
            "create_task": {
                "function": self.create_task,
                "args": {
                    "epic_id": "str required",
                    "description": "str required",
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

    def create_task(self, epic_id: str, description: str):

        self.task_service.create(epic_id, description)
