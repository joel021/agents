
import typing_extensions as typing

from agents.db.task import Task



class Instruction(typing.TypedDict):

    function_name: str
    args: dict
    summary: str
    next_tasks: list[Task]

    def __init__(self, function_name: str, args: dict, summary: str, next_tasks: list[dict]):
        self.function_name: str = function_name
        self.args: dict = args
        self.summary: str = summary
        self.next_tasks: list[dict] = next_tasks

