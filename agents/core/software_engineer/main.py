from redis import Redis
from agents.core.actuator.redis_comm import publish_message
from agents.core.dto.message_dto import MessageDTO
from agents.config import GEMINI_API_KEY
import google.generativeai as genai
from agents.constants import SOFTWARE_ENGINEER_NAME, DEVELOPER_SPECIALIST_AGENT_NAME
from agents.core.software_engineer.model_settings import MODEL_NAME, SAFETY_SETTINGS
from agents.core.software_engineer.input_prompts import create_prompts_prompt, review_code_prompt


if not GEMINI_API_KEY:
    raise Exception("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

class SoftwareEngineer:
    def __init__(self, redis_instance: Redis, task_service):
        self.model = genai.GenerativeModel(MODEL_NAME, safety_settings=SAFETY_SETTINGS)
        self.task_service = task_service
        self.redis_instance = redis_instance
    
    def send_message(self, recipient: str, message: str):

        message_dict = MessageDTO(
            sender=SOFTWARE_ENGINEER_NAME,
            recipient=recipient,
            message=message,
        ).to_dict()
        publish_message(self.redis_instance, message_dict)

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
        if not message or not message.get('recipient', None) == SOFTWARE_ENGINEER_NAME:
            print("Empty message or incorrect recipient")
            return False
        
        data = message.get('data', None)
        task_id = data.get('id', None) if data else None
        task = self.task_service.get_by_id(task_id) if task_id else None

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
