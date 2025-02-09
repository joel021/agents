import os
from multiprocessing import Process

from mongoengine import connect
from agents.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, WORK_DIR
from agents.core.os_agent.os_agent_handler import start_os_agent
from agents.core.research_agent.research_agent_handler import start_researcher_agent
from agents.core.user_agent import start_user_interaction


def start_parallel_processes(tasks: list[dict]):

    for task in tasks:
        process = Process(target=task['function'], kwargs=task['args'])
        process.start()

def main():

    processes = [
        {
            "function": start_os_agent,
            "args": {}
        },
        {
            "function": start_researcher_agent,
            "args": {}
        }
    ]

    connect(db=DB_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT),
            authentication_source='admin')

    os.makedirs(WORK_DIR, exist_ok=True)

    start_parallel_processes(processes)

    #The last process is the User agent. It must be executed in the main thread to allow the user inputs.
    start_user_interaction()

if __name__ == "__main__":

    main()

