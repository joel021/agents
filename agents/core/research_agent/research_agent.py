import json
from redis import Redis
from agents.config import RESEARCH_AGENT_NAME, REDIS_CHANNEL
from agents.constants import PROJECT_MANAGER_AGENT_NAME, OPERATION_SYSTEM_AGENT_NAME
from agents.core.dto.response import Response
from agents.core.llm_reasoner import LLMReasoner
from agents.core.message import Message
from agents.utils.redis_utils import publish_message
from agents.utils.web import search_web 

ALLOWED_SENDERS = {PROJECT_MANAGER_AGENT_NAME, OPERATION_SYSTEM_AGENT_NAME}

class ResearchAgent:
    def __init__(self, llm: LLMReasoner, redis_instance: Redis):
        self.llm = llm
        self.redis_instance = redis_instance

    def send_message(self, recipient: str, message: dict,data: dict):
        message_str = json.dumps(Message(
            sender=RESEARCH_AGENT_NAME,
            recipient=recipient,
            message=message,
            data= data
        ).to_dict())
        publish_message(self.redis_instance, REDIS_CHANNEL, message_str)

    def reason(self, message: dict):
        if message['recipient'] != RESEARCH_AGENT_NAME or message['sender'] not in ALLOWED_SENDERS:
            return
        
        query = message['message']
        results = search_web(query)  
        
        if not results:
            response = Response(msg=f"No relevant results found for query: {query}", error=True)
        else:
            response = Response(msg=f"Results for query: {query}", error=False)
            response.data = results
        
        self.send_message(message['sender'],RESEARCH_AGENT_NAME, query,{ "msg": response.msg,
            "error": response.error,
            "data": getattr(response, "data", None)
        })
