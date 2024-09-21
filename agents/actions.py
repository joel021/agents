import subprocess
import os

from agents.response import Response


class Actions:


    def __init__(self):

        self.actions = {

            "execute_terminal": {
                "function": self.execute_terminal,
                "args": {
                    "path": "str required",
                    "command": "str required"
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
