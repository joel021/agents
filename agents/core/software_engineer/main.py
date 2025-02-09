import google.generativeai as genai
import os

# Configure the Gemini API key and model settings.
# GOOGLE_API_KEY = os.getenv("AIzaSyBgTdZNlXRyk0ZFm8Af9kw4x82Y4c0Xixg")  # Set your API key in the environment variable
GOOGLE_API_KEY = "AIzaSyBgTdZNlXRyk0ZFm8Af9kw4x82Y4c0Xixg"  # Set your API key in the environment variable
if not GOOGLE_API_KEY:
    raise Exception("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = 'gemini-1.0-pro'  # Adjust as needed
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

class SoftwareEngineer:
    def __init__(self, name="Software Engineer", expertise="Full-stack"):
        self.name = name
        self.expertise = expertise
        self.model = genai.GenerativeModel(MODEL_NAME, safety_settings=SAFETY_SETTINGS)

    def review_code_from_developer(self, code, task_description, project_context):
        prompt = f"""You are a senior software engineer reviewing code produced by a junior developer. Your role is to provide constructive feedback focusing on code quality, potential bugs, and adherence to best practices.
        
Task Description: {task_description}

Project Context: {project_context}

Code to Review:
{code}

Provide your feedback concisely, without rewriting the code."""
        response = self.model.generate_content(prompt)
        return response.text

    def suggest_testing_strategy(self, task_description, code_design, project_context):
        prompt = f"""You are a senior software engineer advising on testing strategies for a new feature.
        
Task Description: {task_description}

Code Design: {code_design}

Project Context: {project_context}

Suggest a comprehensive testing strategy (unit tests, integration tests, etc.) with specific test cases to consider."""
        response = self.model.generate_content(prompt)
        return response.text

    def identify_potential_risks(self, task_description, proposed_solution, project_context):
        prompt = f"""You are a senior software engineer tasked with identifying potential technical risks for a proposed solution.
        
Task Description: {task_description}

Proposed Solution: {proposed_solution}

Project Context: {project_context}

List potential technical risks and propose mitigation strategies."""
        response = self.model.generate_content(prompt)
        return response.text

    def advise_on_best_practices(self, area_of_concern, project_context):
        prompt = f"""You are a senior software engineer providing advice on best practices regarding {area_of_concern}.
        
Project Context: {project_context}

Offer concise and practical recommendations with examples where applicable."""
        response = self.model.generate_content(prompt)
        return response.text

    def clarify_requirements(self, requirement, project_context):
        prompt = f"""You are a senior software engineer seeking clarification on a project requirement.
        
Requirement: {requirement}

Project Context: {project_context}

List clarifying questions to ensure the requirement is fully understood, considering edge cases and potential implementation challenges."""
        response = self.model.generate_content(prompt)
        return response.text

    def estimate_complexity(self, task_description, project_context):
        prompt = f"""You are a senior software engineer estimating the complexity of a task.
        
Task Description: {task_description}

Project Context: {project_context}

Estimate the complexity (low, medium, high) and provide a rough time estimate. Explain your reasoning briefly."""
        response = self.model.generate_content(prompt)
        return response.text

    def resolve_tasks(self, project_state, code_snippet):
        prompt = f"""You are the Software Engineer agent responsible for resolving tasks in a project.
        
Project State:
- active_project: {project_state['active_project']}
- tasks_assigned: {project_state['tasks_assigned']}
- tasks_ready: {project_state['tasks_ready']}
- code_received: {code_snippet}

Instructions:
1. Validate the received code.
2. If the code is totally valid, output 'Resolved'.
3. If it's partially valid, but needs some feed back, output 'Resolved' and 'Feedback: [your feedback].
4. If the code is totally invalid, output 'Feedback: [your feedback]'.
5. If, after receiving code, you need to suggest changes to the project overall properties or task order, please, output 'Recommendation for project: [your recommendation for the Project Manager]'

What is your decision?
"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def create_prompts(self, project_state, task):
        se_prompt = f"""You're a senior software engineer responsible for using a generative LLM code generator to resolve tasks assigned to you.
        Right now, you have to resolve the following task: {task['title']}
        This is its description: {task['description']}
        Each prompt and corresponding generated code will be back and forth untill you're satisfied with the prompt's output.
        Please, generate a prompt or a list of prompts to resolve that task completely. Output prompts only, each in its own line for easier extraction.
        """
        response = self.model.generate_content(se_prompt)
        return response.text

# Example Usage
if __name__ == '__main__':
    engineer = SoftwareEngineer(name="Alice")

    # Example: Resolve Tasks
    project_state = {
        "active_project": True,
        "tasks_assigned": True,
        "tasks_ready": True
    }
    # code_snippet = "def calculate_sum(a, b): return a * b"
    # decision = engineer.resolve_tasks(project_state, code_snippet)
    task = {
    'id': '#005',
    'title': 'Implement Matrix Multiplication',
    'description': (
        'Create a Python function that multiplies two matrices. '
        'The function should first validate the dimensions, then perform the multiplication, '
        'and finally return the resulting matrix. Generate separate prompts for each step: '
        'validation, multiplication, and formatting the result.'
    )
}
    decision = engineer.create_prompts(project_state, task)
    prompts = decision.split('\n')
    print("Decision for Resolve Tasks:\n", decision)

    model = genai.GenerativeModel(MODEL_NAME, safety_settings=SAFETY_SETTINGS)
    for prompt in prompts:
        #placeholder for DS
        response = model.generate_content(prompt)
        print(response.text)


    # You can uncomment and test other methods as needed:
    # review_feedback = engineer.review_code_from_developer(code_snippet, "Calculate sum function", "Math utility module")
    # print("\nCode Review Feedback:\n", review_feedback)
    
    # testing_strategy = engineer.suggest_testing_strategy("User authentication with JWTs", "Flask-JWT-Extended integration", "API for web application")
    # print("\nTesting Strategy:\n", testing_strategy)
    
    # risks = engineer.identify_potential_risks("Integrate with payment gateway", "Using the official API with webhooks", "E-commerce platform")
    # print("\nPotential Risks:\n", risks)
    
    # best_practices = engineer.advise_on_best_practices("API security", "Mobile app backend")
    # print("\nBest Practices for API Security:\n", best_practices)
    
    # clarification = engineer.clarify_requirements("Implement a user profile page", "Main web application with sensitive user data")
    # print("\nClarification Questions:\n", clarification)
    
    # complexity = engineer.estimate_complexity("Implement profile picture upload with cropping", "Desktop and mobile support", "Social media application")
    # print("\nComplexity Estimate:\n", complexity)
