from agents.core.agents_switch import AgentSwitch
from agents.core.dto.llm_schema import BreakTaskIntoInstructionsSchema
from agents.core.performer.instruction_performer import InstructionPerformer
from agents.core.instructions_handler import InstructionsHandler
from agents.core.dto.response import Response
from agents.db.service.story_service import StoryService
from agents.db.service.task_service import TaskService
from agents.db.status import Status
from agents.db.task import Task
from agents.logger import logger


class TaskPerformer:

    def __init__(self, agent_switch: AgentSwitch, task_service: TaskService, story_service: StoryService):
        self.task_service = task_service
        self.story_service = story_service
        self.llm_handler = agent_switch.get_llm_agent()
        self.instructions_handler = InstructionsHandler()

    def instruction_to_str(self, instructions: list[dict]) -> list[str]:

        return [instruction['title'] for instruction in instructions]

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

        while instructions:
            instruction = instructions.pop(0)
            current_result = self._execute_single_instruction(instruction, results, performed_instructions)

            if current_result.error:
                break

            feedback = self._get_feedback(task, results, current_result, instructions)
            instructions, summary = self._update_instructions_and_summary(feedback, instructions, story_id, summary)

        return self._finalize_execution(task, summary, performed_instructions, current_result)

    def _execute_single_instruction(self, instruction, results, performed_instructions):
        """Execute a single instruction and log the result."""
        current_result = self.instructions_handler.execute_instruction(instruction)
        results.append({
            "instruction": instruction,
            "result": current_result
        })

        if current_result.error:
            logger.info(f"Error occurred while executing instruction: {current_result.msg}")
        else:
            performed_instructions.append(instruction)

        return current_result

    def _get_feedback(self, task, results, current_result, instructions):
        """Generate feedback from the LLM based on the current task state."""
        feedback_prompt = (
            f'Task specification: {task.specification}. '
            f'We have completed the following instructions: {results}. '
            f'The result of the last instruction was: {current_result}. '
            f'We are going to execute the following instructions: ```{self.instruction_to_str(instructions)}```. '
            f'Adjust the remaining instructions if necessary. Summarize the completed instructions. '
            f'The available instructions/functions are: {InstructionPerformer.get_available_instructions_str()}. '
        )
        return self.llm_handler.generate_instructions_dict(feedback_prompt, BreakTaskIntoInstructionsSchema)

    def _update_instructions_and_summary(self, feedback, instructions, story_id, summary):
        """Update instructions and summary based on feedback."""
        updated_instructions = feedback.get("instructions", instructions)
        new_tasks = feedback.get("new_tasks", [])

        if new_tasks:
            self.story_service.create_tasks_to_story_id(story_id, new_tasks)

        updated_summary = feedback.get("summary", summary)

        return updated_instructions, updated_summary

    def _finalize_execution(self, task, summary, performed_instructions, current_result):
        """Finalize task execution, updating the task object and ensuring a result."""
        if not current_result:
            current_result = Response("No tasks performed.", False)

        task = self.task_service.set_summary(task, summary)
        task = self.task_service.set_instructions(task, performed_instructions)

        return current_result, task

    def try_solve(self, task: Task, prompt: str, story_id: str, summary: str) -> tuple[Response, Task]:

        initial_instructions_dict = self.llm_handler.generate_instructions_dict(prompt,
                                                                                BreakTaskIntoInstructionsSchema)
        initial_instructions = initial_instructions_dict.get("instructions", [])
        self.story_service.create_tasks_to_story_id(story_id, initial_instructions_dict.get("new_tasks", []))
        resp, task = self.execute_instructions_dynamically(task, story_id, initial_instructions, summary)

        return resp, task

    def perform(self, task: Task, story_id: str, summary: str) -> Task:
        """
        Perform a task by breaking it down into instructions and dynamically updating the instructions as needed.
        """
        self.task_service.set_status(task, Status.IN_PROGRESS)

        prompt = (
            f'Using the available instructions, solve the following task: story_id={story_id}, '
            f'task title = {task.title}, task specification = {task.specification}. '
            f'The available instructions/functions are: {InstructionPerformer.get_available_instructions_str()}. '
            f'Break it down into more tasks, in new_tasks, if the task is too complex. '
            f'We have completed: {summary}'
        )

        resp, task = self.try_solve(task, prompt, story_id, summary)

        if resp.error:
            return self.task_service.set_status(task, Status.ERROR)

        return self.task_service.set_status(task, Status.DONE)
