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

    def to_dict(self):

        return {
            'title': self.title,
            'status': str(self.status).upper(),
            'specification': self.specification,
            'instructions': entity_list_to_dict_list(self.instructions),
            'summary': self.summary,
        }
