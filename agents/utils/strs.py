
def instruction_to_str(instructions: list[dict]) -> list[str]:
    return [instruction.get('title', "") for instruction in instructions]
