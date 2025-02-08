from agents.core.agents_switch import AgentSwitch
from agents.core.os_agent.operation_system_agent import OperationSystemAgent
from agents.core.dto.response import Response
from agents.core.planner import Planner
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.task import Task
from agents.logger import logger


class TaskPerformer:

    def __init__(self, agent_switch: AgentSwitch, task_service: TaskService, story_service: StoryService):
        self.task_service = task_service
        self.story_service = story_service
        self.instructions_handler = OperationSystemAgent()
        self.planner = Planner(agent_switch.get_llm_agent(), story_service)

    def execute_instructions_dynamically(self, task: Task, story_id: str, initial_instructions: list,
                                         summary: str) -> tuple[Response, Task]:
        """
        Execute instructions dynamically, updating the instruction set after each one based on feedback from the LLM.
        """
        instructions = initial_instructions
        results = []
        current_result = None
        summary = summary
        performed_instructions = []

        tries = 0

        while instructions:
            instruction = instructions.pop(0)
            current_result = self._execute_single_instruction(instruction, results, performed_instructions)

            if current_result.error:

                if tries > 3:
                    break

                tries += 1
                logger.error(current_result.msg)
                instructions, summary = self.planner.replan(task, results, instructions, story_id, summary)

        return self._finalize_execution(task, summary, performed_instructions, current_result)

    def _execute_single_instruction(self, instruction, results, performed_instructions):
        """Execute a single instruction and log the result."""
        current_result = self.instructions_handler.execute_instruction(instruction)
        results.append({
            "instruction": instruction,
            "result": current_result
        })

        print(f"Executing instruction: {instruction}\n result: {current_result}")

        if not current_result.error:
            performed_instructions.append(instruction)

        return current_result

    def _finalize_execution(self, task, summary, performed_instructions, current_result):
        """Finalize task execution, updating the task object and ensuring a result."""
        if not current_result:
            current_result = Response("No tasks performed.", False)

        task = self.task_service.set_summary(task, summary)
        task = self.task_service.set_instructions(task, performed_instructions)

        return current_result, task

    def try_solve(self, task: Task, story_id: str, summary: str) -> tuple[Response, Task]:

        initial_instructions_dict = self.planner.plan(task, story_id, summary)
        initial_instructions = initial_instructions_dict.get("instructions", [])
        self.story_service.create_tasks_to_story_id(story_id, initial_instructions_dict.get("new_tasks", []))
        resp, task = self.execute_instructions_dynamically(task, story_id, initial_instructions, summary)

        return resp, task

    def perform(self, task: Task, story_id: str, summary: str) -> Task:
        """
        Perform a task by breaking it down into instructions and dynamically updating the instructions as needed.
        """
        self.task_service.set_status(task, Status.IN_PROGRESS)
        resp, task = self.try_solve(task, story_id, summary)

        if resp.error:
            return self.task_service.set_status(task, Status.ERROR)

        return self.task_service.set_status(task, Status.DONE)
