import typing_extensions as typing


class StoryResponse(typing.TypedDict):
    title: str
    specification: str


class TaskResponse(typing.TypedDict):
    title: str
    specification: str


class ArgumentResponse(typing.TypedDict):

    arg_key: str
    value: str


class InstructionResponse(typing.TypedDict):
    function_name: str
    arguments: typing.List[ArgumentResponse]


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


class BreakTaskIntoInstructionsResponse(typing.TypedDict):
    instructions: typing.List[InstructionResponse]
    summary: str
    next_tasks: typing.List[TaskResponse]

