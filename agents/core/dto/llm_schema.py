import typing_extensions as typing


class StorySchema(typing.TypedDict):
    title: str
    specification: str

    def __init__(self, title: str, specification: str):
        self.title = title
        self.specification = specification


class TaskSchema(typing.TypedDict):
    title: str
    specification: str

    def __init__(self, title: str, specification: str):
        self.title = title
        self.specification = specification


class ArgumentSchema(typing.TypedDict):
    arg: str
    value: str

    def __init__(self, arg: str, value: str):
        self.arg = arg
        self.value = value


class InstructionSchema(typing.TypedDict):
    function_name: str
    arguments: typing.List[ArgumentSchema]

    def __init__(self, function_name: str, arguments: typing.List[ArgumentSchema]):
        self.function_name = function_name
        self.arguments = arguments


class BreakEpicIntoStoriesSchema(typing.TypedDict):
    """
    ```{"summary": "summarize what have done", "new_stories": [{"title": "story title 1",'
                         '"specification":"..."},...]}```
    """
    summary: str
    new_stories: typing.List[StorySchema]

    def __init__(self, summary: str, new_stories: typing.List[StorySchema]):
        self.summary = summary
        self.new_stories = new_stories


class BreakStoryIntoTasksSchema(typing.TypedDict):
    summary: str
    new_tasks: typing.List[TaskSchema]

    def __init__(self, summary: str, new_tasks: typing.List[TaskSchema]):
        self.summary = summary
        self.new_tasks = new_tasks


class GenerateOSInstructionsSchema(typing.TypedDict):

    valid: bool
    instructions: typing.List[InstructionSchema]
    summary: str
    next_tasks: typing.List[TaskSchema]

    def __init__(self, instructions: typing.List[InstructionSchema], summary: str, next_tasks: typing.List[TaskSchema]):
        self.instructions = instructions
        self.summary = summary
        self.next_tasks = next_tasks
