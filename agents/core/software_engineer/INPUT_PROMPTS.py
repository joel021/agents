def create_prompts_prompt(task):
    se_prompt = f"""You're a senior software engineer responsible for using a generative LLM code generator to resolve tasks assigned to you.
            Your role is to craft a well engineered prompt so it'll be sent to an LLM that will generate the respective code for it.
            Right now, you have to resolve the following task: {task['title']}
            This is its description: {task['description']}
            Instructions
            1. Output prompt only for easier extraction, please.
            2. Include in your prompt you want a code only output, please.
            """
    return se_prompt


def review_code_prompt(task, code):
    prompt = f"""You are a senior software engineer reviewing code produced by a junior developer. Your role is to provide constructive feedback focusing on code quality, potential bugs, and adherence to best practices.
        
Task Description: {task['description']}

Code to Review:
{code}

Provide your feedback concisely, without rewriting the code."""