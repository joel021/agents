from agents.core.pm_agent.agent_handler import AgentHandler


class AgentsController:


    def __init__(self, agents: AgentHandler):
        self.agents = agents

    async def execute_open_epocs(self):

        self.agents.execute_open_epics()

        return "Epocs are being executed", 201
