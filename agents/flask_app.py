from flask import Flask, request

from agents.api.epic_controller import EpicController
from agents.db.service.epic_service import EpicService

app = Flask(__name__)

epic_service = EpicService()
epic_controller = EpicController(epic_service)
@app.route('/epic', methods=['POST'])
def create_entity():
    data = request.json
    return epic_controller.create_epic(data)

@app.route('/epic/<id>', methods=['GET'])
def get_epic(id):
    return epic_controller.get_epic(id)

@app.route('/epic/<id>', methods=['DELETE'])
def delete_entity(id):
    return epic_controller.delete_epic(id)
