# Auto software engineer multi agents using a large language model

This is a Python project using poetry as dependency management. Below are the instructions for running it.

- Suggestion to use linux
- Install any python 3
- Install poetry globally to your python 3 $ ```pip3 install poetry```
- Set poetry to create env in the project: $ ```poetry config virtualenvs.in-project true```
- Activate the python environment $ ```poetry shell```
- Install dependencies $ ```poetry install```
- Install postgres database managament
- Create a .env based on the .env.example file
- Run the python project with ```python run agents/__main__.py```
- Tests are in /tests folder, run them with ```python -m unittest```
