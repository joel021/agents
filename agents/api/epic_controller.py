from flask import jsonify

from agents.db.service.epic_service import EpicService


class EpicController:

    def __init__(self, epic_service: EpicService):
        self.epic_service = epic_service

    def create_epic(self, data: dict):
        try:
            epic_created = self.epic_service.create(data)
            return jsonify(epic_created.to_dict()), 201
        except Exception as e:
            print(e)
            return jsonify({'error': 'Internal error encountered.'}), 400

    def get_epic(self, id: str):
        try:
            return jsonify(self.epic_service.find_by_id(id)), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'Not found.'}), 404

    def delete_epic(self, id: str):
        try:
            self.epic_service.delete(id)
            return jsonify({'message': 'Deleted successfully!'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'Entity not found'}), 404
