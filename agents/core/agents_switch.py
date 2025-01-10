from agents.config import GEMINI_API_KEY, GPT_API_KEY
from agents.core.llm_handler import GeminiHandler


class AgentSwitch:

    def __init__(self, single_agent: bool):
        self.single_agent = single_agent
        self.agent = None

    def get_llm_agent(self):

        if self.single_agent:

            if not self.agent:
                self.agent = self.get_new_llm_agent()
            return self.agent

        return self.get_new_llm_agent()

    def get_new_llm_agent(self):

        if GEMINI_API_KEY:
            return GeminiHandler(GEMINI_API_KEY)
        elif GPT_API_KEY:
            raise NotImplementedError("Gpt interfaces were not implemented yet.")

        raise NotImplementedError("No other options unless Gemini are available. Fill the GEMINI_API_KEY value.")
