from mongoengine import StringField, ListField, ReferenceField, Document, EnumField

from agents.db.status import Status
from agents.db.task import Task


class Story(Document):

    status = EnumField(Status, default=Status.TODO)
    description = StringField()
    tasks = ListField(ReferenceField(Task))

    def is_done(self):

        is_done = True
        for task in self.tasks:
            is_done = is_done and task.is_done

        return is_done
