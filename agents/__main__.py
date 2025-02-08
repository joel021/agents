import os

from joblib import Parallel, delayed
from mongoengine import connect
from agents.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, WORK_DIR
from agents.core.os_agent.os_agent_handler import start_os_agent


def start_parallel_processes(tasks: list[dict], use_threads=False):
    backend = 'threading' if use_threads else 'loky'
    return Parallel(n_jobs=len(tasks), backend=backend)(
        delayed(task['function'])(**task['args']) for task in tasks
    )

def main():

    processes = [
        {
            "function": start_os_agent,
            "args": {}
        }
    ]

    connect(db=DB_NAME, username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=int(DB_PORT),
            authentication_source='admin')

    os.makedirs(WORK_DIR, exist_ok=True)

    start_parallel_processes(processes)

    #the last process is the PM agent, it must be executed in the main thread, to allow the user inputs


if __name__ == "__main__":



    main()

