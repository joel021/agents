from redis import Redis
from agents.constants import PROJECT_MANAGER_AGENT_NAME, OPERATION_SYSTEM_AGENT_NAME, RESEARCH_AGENT_NAME, DEVELOPER_SPECIALIST_AGENT_NAME
from agents.core.dto.response import Response
from agents.core.dto.message_dto import MessageDTO
from agents.core.llm_reasoner import LLMReasoner
from agents.core.actuator.redis_comm import publish_message
from agents.utils.web import search_web 


class ResearchAgent:

    ALLOWED_SENDERS = {PROJECT_MANAGER_AGENT_NAME, OPERATION_SYSTEM_AGENT_NAME,DEVELOPER_SPECIALIST_AGENT_NAME}

    def __init__(self, llm: LLMReasoner, redis_instance: Redis):
        self.llm = llm
        self.redis_instance = redis_instance

    def send_message(self, recipient: str, message: str, data: dict=None):
        message_dict = MessageDTO(
            sender=RESEARCH_AGENT_NAME,
            recipient=recipient,
            message=message,
            data= data
        ).to_dict()
        publish_message(self.redis_instance, message_dict)

    def reason(self, message: dict):

        if (not message or message.get('recipient', None) != RESEARCH_AGENT_NAME
                or message.get('sender', None) not in self.ALLOWED_SENDERS):
            return False
        
        query = message['message']
        results = search_web(query)
        
        if not results:
            response = Response(msg=f"No relevant results found for query: {query}", error=True)
            resp = f"{response.msg}"
            self.send_message(message['sender'], resp)
            return False
        else:
            response = Response(msg=f"Results for query: {query}", error=False)

            formatted_results = "\n".join([f"{r['title']}: {r['snippet']}" for r in results])
            summarized_results = self.llm.simple_answer(formatted_results)
            response.data = summarized_results

        resp = f"{response.msg}"
        data = {
            "action": "research",
            "query": query,
            "results": response.data
        }
        self.send_message(message['sender'], resp, data)
        return True
