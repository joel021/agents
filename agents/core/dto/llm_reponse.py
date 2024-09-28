from typing import List, TypedDict


class StoryResponse(TypedDict):
    title: str
    specification: str

    def __init__(self, title: str, specification: str):
        self.title = title
        self.specification = specification


class TaskResponse(TypedDict):
    title: str
    specification: str

    def __init__(self, title: str, specification: str):
        self.title = title
        self.specification = specification


class ArgumentResponse(TypedDict):
    arg: str
    value: str

    def __init__(self, arg: str, value: str):
        self.arg = arg
        self.value = value


class InstructionResponse(TypedDict):
    function_name: str
    arguments: List[ArgumentResponse]

    def __init__(self, function_name: str, arguments: List[ArgumentResponse]):
        self.function_name = function_name
        self.arguments = arguments


class BreakEpicIntoStoryResponse(TypedDict):
    """
    ```{"summary": "summarize what have done", "new_stories": [{"title": "story title 1",'
                         '"specification":"..."},...]}```
    """
    summary: str
    new_stories: List[StoryResponse]

    def __init__(self, summary: str, new_stories: List[StoryResponse]):
        self.summary = summary
        self.new_stories = new_stories


class BreakStoryIntoTasksResponse(TypedDict):
    summary: str
    new_tasks: List[TaskResponse]

    def __init__(self, summary: str, new_tasks: List[TaskResponse]):
        self.summary = summary
        self.new_tasks = new_tasks


class BreakTaskIntoInstructionsResponse(TypedDict):
    instructions: List[InstructionResponse]
    summary: str
    next_tasks: List[TaskResponse]

    def __init__(self, instructions: List[InstructionResponse], summary: str, next_tasks: List[TaskResponse]):
        self.instructions = instructions
        self.summary = summary
        self.next_tasks = next_tasks
