
class Instruction:

    def __init__(self, function_name: str, args: dict, summary: str, next_tasks: list[dict]):
        self.function_name: str = function_name
        self.args: dict = args
        self.summary: str = summary
        self.next_tasks: list = next_tasks

