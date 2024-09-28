import os
import subprocess

from agents.core.dto.response import Response


def execute_terminal(path: str, command: str):
    path = os.path.expanduser(path)
    process = subprocess.Popen(command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    result = stdout.decode('utf-8')
    if stderr:
        error = stderr.decode('utf-8')
        return Response(error, True)

    return Response(result, False)