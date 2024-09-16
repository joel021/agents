from agents.llm_handler import generate_instructions
from agents.instructions_handler import execute_instructions


def main():
    while True:
        user_prompt = input("Enter your request: ")
        if user_prompt.lower() == "quit":
            break

        instructions = generate_instructions(user_prompt)
        print("Instructions generated:")
        print(instructions)

        execute_instructions(instructions)


if __name__ == "__main__":

    main()