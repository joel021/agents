from redis import Redis
from agents.core.actuator.redis_comm import publish_message
from agents.core.dto.message_dto import MessageDTO
from agents.core.llm_reasoner import LLMReasoner
import google.generativeai as genai
from agents.constants import SOFTWARE_ENGINEER_AGENT_NAME, DEVELOPER_SPECIALIST_AGENT_NAME
from agents.core.software_engineer.model_settings import MODEL_NAME, SAFETY_SETTINGS
from agents.core.software_engineer.input_prompts import create_prompts_prompt, review_code_prompt


# Configure the Gemini API key and model settings.
# GOOGLE_API_KEY = os.getenv("AIzaSyBgTdZNlXRyk0ZFm8Af9kw4x82Y4c0Xixg")  # Set your API key in the environment variable
GOOGLE_API_KEY = "AIzaSyBgTdZNlXRyk0ZFm8Af9kw4x82Y4c0Xixg"  # Set your API key in the environment variable
if not GOOGLE_API_KEY:
    raise Exception("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)

class SoftwareEngineer:
    def __init__(self, redis_instance: Redis, task_service):
        self.model = genai.GenerativeModel(MODEL_NAME, safety_settings=SAFETY_SETTINGS)
        self.task_service = task_service
        self.redis_instance = redis_instance
    
    def send_message(self, recipient: str, message: str):

        message_dict = MessageDTO(
            sender=SOFTWARE_ENGINEER_AGENT_NAME,
            recipient=recipient,
            message=message,
        ).to_dict()
        publish_message(self.redis_instance, message_dict)

    def review_code_from_developer(self, code):
        prompt = review_code_prompt(task, code)
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

    def create_prompts(self, task):
        se_prompt = create_prompts_prompt(task)
        response = self.model.generate_content(se_prompt)
        return response.text
    
    def reason(self, message: dict) -> bool:
        if not message or not message.get('recipient', None) == SOFTWARE_ENGINEER_AGENT_NAME:
            print("Empty message or incorrect recipient")
            return False
        
        data = message['data']
        task_id = data.get('id', None)
        task = self.task_service.get_by_id(task_id)

        prompt = self.create_prompts(task)

        if prompt:
            self.send_message(DEVELOPER_SPECIALIST_AGENT_NAME, prompt)
            return True
        else:
            resp = (
                f"I could not attend to the message: {message['message']}."
            )
            self.send_message(message['sender'], resp)
            return False
    

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
        'and finally return the resulting matrix.'
    )
}
    se_prompt = engineer.create_prompts(project_state, task)
    print("Decision for create_prompts:\n", se_prompt)

    model = genai.GenerativeModel(MODEL_NAME, safety_settings=SAFETY_SETTINGS)
    #for prompt in prompts:
    #placeholder for DS
    response = model.generate_content(se_prompt)
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
