# Auto software engineer multi agents using a large language model

This is a Python project using poetry as dependency management. Below are the instructions for running it.

- Suggestion to use linux
- Install docker desktop https://www.docker.com/products/docker-desktop/
- Execute docker desktop
- Install any python 3
- Install poetry globally to your python 3 $ ```pip3 install poetry```
- Set poetry to create env in the project: $ ```poetry config virtualenvs.in-project true```
- Activate the python environment $ ```poetry shell```
- Install dependencies $ ```poetry install```
- On the same level of ```docker-compose.yml``` file, run ```docker compose up```
- Create a .env based on the .env.example file
- Run the python project with ```python run agents/__main__.py```
- Tests are in /tests folder, run them with ```python -m unittest```

Project structure

- agents/core: main package of the project
- agents/actuator: scripts that treats the actuators and perceptions of the agents
- agents/dto: data transfer objects definitions
- agents/os_agent: operation system agent
- agents/pm_agent: project manager agent
- agents/research_agent: researcher agents
- agents/db: treats the database management of the system
- tests: where the automated tests are implemented

How does it works?

Each agent is started as a separate process which they listen and send message to a shared chanel of redis service.
The Project Manager has communication with the user and command other agents.


