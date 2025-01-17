
from agents.core.dto.llm_schema import BreakTaskIntoInstructionsSchema
from agents.core.dto.response import Response
from agents.core.llm_handler import LLMHandler
from agents.core.performer.instruction_performer import InstructionPerformer
from agents.db.service.story_service import StoryService
from agents.db.task import Task
from agents.utils.strs import instruction_to_str


class Planner:

    def __init__(self, llm_handler: LLMHandler, story_service: StoryService):

        self.llm_handler = llm_handler
        self.story_service = story_service

    def plan(self, task: Task, story_id: str, summary: str):
        prompt = (
            f'Using the available instructions, solve the following task: story_id={story_id}, '
            f'task title = {task.title}, task specification = {task.specification}. '
            f'The available instructions/functions are: {InstructionPerformer.get_available_instructions_str()}. '
            f'Break it down into more tasks, in new_tasks, if the task is too complex. '
            f'We have completed: {summary}'
        )
        instructions_dict = self.llm_handler.generate_instructions_dict(prompt,
                                                                        BreakTaskIntoInstructionsSchema)
        return instructions_dict

    def replan(self, task: Task, results: list[Response], instructions: list[dict],
               story_id: str, summary: str) -> tuple[list[dict], str]:

        feedback = self._get_feedback(task, results, instructions)
        instructions, summary = self._update_instructions_and_summary(feedback, instructions, story_id, summary)

        return instructions, summary

    def _get_feedback(self, task: Task, results: list[Response], instructions: list[dict]):
        """Generate feedback from the LLM based on the current task state."""
        feedback_prompt = ('You are a software engineering developer. '
            f'Task specification: {task.specification}. '
            f'We have completed the following instructions: {results}. '
            f'We were going to execute the following instructions: ```{instruction_to_str(instructions)}```. '
            'Summary the what have been done and explain encountered problem to help another '
                           'software engineering developer solve the problem and continue the task.'
        )
        summary = self.llm_handler.summary(feedback_prompt)
        replan_prompt = ('You are a software engineering developer. '
                         f"Task specification: {task.specification}. "
                         f"{summary}"
                         f'Adjust the instructions due to the encountered problem. '
                         f'Bring a summary to help another developer continue the work.'
            f'The available instructions/functions are: {InstructionPerformer.get_available_instructions_str()}.')

        return self.llm_handler.generate_instructions_dict(replan_prompt, BreakTaskIntoInstructionsSchema)

    def _update_instructions_and_summary(self, feedback: dict, instructions, story_id, summary):
        """Update instructions and summary based on feedback."""
        updated_instructions = feedback.get("instructions", instructions)
        new_tasks = feedback.get("new_tasks", [])

        if new_tasks:
            self.story_service.create_tasks_to_story_id(story_id, new_tasks)

        updated_summary = feedback.get("summary", summary)

        return updated_instructions, updated_summary
