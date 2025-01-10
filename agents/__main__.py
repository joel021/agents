import os

from mongoengine import connect

from agents.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, WORK_DIR, SINGLE_AGENTS
from agents.core.agent_handler import AgentHandler
from agents.core.agents_switch import AgentSwitch


def main():

    connect(db=DB_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT),
            authentication_source='admin')

    os.makedirs(WORK_DIR, exist_ok=True)

    AgentHandler(AgentSwitch(SINGLE_AGENTS)).execute_open_epics()


if __name__ == "__main__":

    main()

