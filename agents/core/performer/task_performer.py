from agents.core.dto.llm_reponse import BreakTaskIntoInstructionsResponse
from agents.core.performer.instruction_performer import InstructionPerformer
from agents.core.instructions_handler import InstructionsHandler
from agents.core.llm_handler import LLMHandler
from agents.core.dto.response import Response
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.task import Task
from agents.logger import logger


class TaskPerformer:

    def __init__(self, llm_handler: LLMHandler, task_service: TaskService, story_service: StoryService):
        self.task_service = task_service
        self.story_service = story_service
        self.llm_handler = llm_handler
        self.instructions_handler = InstructionsHandler(task_service)
        self.prefix = ('Answer following the json structure: {"instructions": [{"function_name": "function name", '
                       '"args":{"arg1":"v1", "arg2": "v2", ...}}, ...], "summary": "summarize the instructions", '
                       '"new_tasks": [{"title": "task 1", "specification": "specifications"}, {"title": "task 2", '
                       '"specification": "specifications"}, ...]}.')
        self.max_tries = 3

    def execute_task(self, task: Task, prompt: str, story_id: str) -> tuple[Response, Task]:

        instructions_dict = self.llm_handler.generate_instructions_dict(prompt, BreakTaskIntoInstructionsResponse)
        self.story_service.create_tasks_to_story_id(story_id, instructions_dict.get("new_tasks", []))
        task = self.task_service.set_summary(task, instructions_dict.get("summary", ""))
        resp = self.instructions_handler.execute_instructions(instructions_dict.get("instructions", []))

        return resp, task

    def try_solve(self, task: Task, prompt: str, story_id: str, summary: str) -> tuple[Response, Task]:

        resp, task = self.execute_task(task, prompt, story_id)

        tries = 0
        while resp.error:
            tries += 1
            logger.info(f"Error when performing task {task.id}")
            prompt = (f'I received the error {resp.msg} when performing {task.title}, specified '
                      f'as {task.specification}. We have done: {summary}')
            resp, task = self.execute_task(task, prompt, story_id)
            if tries >= self.max_tries:
                logger.info(f"Error ```{resp.msg}``` not solved.")
                break
        return resp, task

    def perform(self, task: Task, story_id: str, summary: str) -> Task:

        self.task_service.set_status(task, Status.IN_PROGRESS)

        prompt = (f'Solve the following task using the available instructions: story_id={story_id},'
                  f' task title = {task.title}, task specification = f{task.specification}. '
                  f'The available instructions/functions are: {InstructionPerformer.get_available_instructions_str()}. '
                  f'Break it down into more tasks, in new_tasks, If the task is too complex. We have done: {summary}')

        resp, task = self.try_solve(task, prompt, story_id, summary)

        if resp.error:
            return self.task_service.set_status(task, Status.ERROR)

        return self.task_service.set_status(task, Status.DONE)
