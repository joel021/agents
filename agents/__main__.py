import os

from mongoengine import connect

from agents.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, WORK_DIR, SINGLE_AGENTS
from agents.core.agent_handler import AgentHandler


def main():
    db_connection_string = (f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    connect(db_connection_string)

    os.makedirs(WORK_DIR, exist_ok=True)

    AgentHandler(SINGLE_AGENTS).execute_open_epics()


if __name__ == "__main__":

    main()

