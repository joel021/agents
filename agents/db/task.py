from mongoengine import Document, ListField, DictField, StringField, EnumField

from agents.db.data_model import DataModel, entity_list_to_dict_list
from agents.db.status import Status


class Task(DataModel, Document):

    title = StringField()
    status = EnumField(Status, default=Status.TODO)
    specification = StringField() #What to do
    instructions = ListField(DictField()) #Set of instructions performed
    summary = StringField() #How have done

    def is_done(self):
        return self.status == Status.DONE

    @staticmethod
    def from_dict(data: dict) -> 'Task':

        if data.get('id', None):
            task = Task(
                id=data['id'],
                title=data.get('title', None),
                status=Status.from_keyword(data.get('status', Status.TODO.name)),
                specification=data.get('specification', None),
                instructions=data.get('instructions', None),
                summary=data.get('summary', None),
            )
        else:
            task = Task(
                title=data.get('title', None),
                status=Status.from_keyword(data.get('status', Status.TODO.name)),
                specification=data.get('specification', None),
                instructions=data.get('instructions', None),
                summary=data.get('summary', None),
            )
        return task

    def to_dict(self):

        return {
            'id': self.id,
            'title': self.title,
            'status': str(self.status).upper(),
            'specification': self.specification,
            'instructions': entity_list_to_dict_list(self.instructions),
            'summary': self.summary,
        }
