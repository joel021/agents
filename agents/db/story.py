from mongoengine import StringField, ListField, ReferenceField, Document, EnumField

from agents.db.data_model import DataModel, entity_list_to_dict_list
from agents.db.status import Status
from agents.db.task import Task


class Story(DataModel, Document):

    title = StringField()
    status = EnumField(Status, default=Status.TODO)
    description = StringField()
    tasks = ListField(ReferenceField(Task))
    summary = StringField()

    def is_done(self):

        is_done = True
        for task in self.tasks:
            is_done = is_done and task.is_done

        return is_done

    def to_dict(self):

        return {
            'title': self.title,
            'status': str(self.status).upper(),
            'description': self.description,
            'tasks': entity_list_to_dict_list(self.tasks),
            'summary': self.summary,
        }
