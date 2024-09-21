from mongoengine import StringField, ListField, ReferenceField, Document

from agents.db.task import Task


class Story(Document):

    description = StringField()
    tasks = ListField(ReferenceField(Task))
