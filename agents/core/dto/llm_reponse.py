import typing_extensions as typing


class StoryResponse(typing.TypedDict):
    title: str
    specification: str


class TaskResponse(typing.TypedDict):
    title: str
    specification: str


class BreakEpicIntoStoryResponse(typing.TypedDict):
    """
    ```{"summary": "summarize what have done", "new_stories": [{"title": "story title 1",'
                         '"specification":"..."},...]}```
    """
    summary: str
    new_stories: typing.List[StoryResponse]


class BreakStoryIntoTasksResponse(typing.TypedDict):
    summary: str
    new_tasks: typing.List[TaskResponse]


class InstructionResponse(typing.TypedDict):
    function_name: str
    args: dict
    summary: str
    next_tasks: list[TaskResponse]

    def __init__(self, function_name: str, args: dict, summary: str, next_tasks: list[TaskResponse]):
        self.function_name: str = function_name
        self.args: dict = args
        self.summary: str = summary
        self.next_tasks: list[dict] = next_tasks
