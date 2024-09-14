import unittest
from llm_handler import generate_instructions
import openai  # Mocked for testing
import pyautogui  # Mocked for testing
import time  # Mocked for testing

# Replace these with mocks or your actual API key/functions
openai.api_key = "YOUR_OPENAI_API_KEY"
action_functions = {
    "click_on": lambda **kwargs: print(f"Clicking at ({kwargs['x']}, {kwargs['y']})")
}

def execute_instructions(instructions: str):
    """Executes the generated instructions using PyAutoGUI."""
    action = instructions.get("action")
    if not action:
        return

    action_method = action_functions.get(action)
    if not action_method:
        print(f"Unsupported action: {action}")
        return

    expected_args = instructions.get("args", {})
    args = {k: v for k, v in expected_args.items() if v is not None}  # Filter out None values

    try:
        action_method(**args)
    except Exception as e:
        print(f"Error executing instructions: {e}")


def main():
    while True:
        user_prompt = input("Enter your request: ")
        if user_prompt.lower() == "quit":
            break

        instructions = generate_instructions(user_prompt)
        print("Instructions generated:")
        print(instructions)

        execute_instructions(instructions)