from agents.db.task import Task


def create_prompts_prompt(task: Task):
    se_prompt = f"""You're a senior software engineer responsible for using a generative LLM code generator to resolve tasks assigned to you.
            Your role is to craft a well engineered prompt so it'll be sent to an LLM that will generate the respective code for it.
            Right now, you have to resolve the following task: {task['title']}
            This is its description: {task['specification']}
            Instructions
            1. Output prompt only for easier extraction, please.
            2. Include in your prompt you want a code only output, please.
            """
    return se_prompt
